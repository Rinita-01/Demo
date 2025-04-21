from django.shortcuts import render, get_object_or_404, redirect
import razorpay
import time
import requests.exceptions
from django.http import JsonResponse

from buybook import settings
from orders.models import Order
from .models import Payment
from books.models import Book
from cart.models import Cart
from orderitem.models import OrderItem
from users.decoraters import custom_login_required
from django.db.models import F
from django.db import transaction

# Razorpay client initialization
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def payment(request):
    amount = request.POST.get("amount")
    return render(request, "payments/payment.html", {"amount": amount})

@custom_login_required
def order_success(request , order_id):
    order = get_object_or_404(Order, id=order_id )
    return render(request, 'orders/order_success.html', {'order': order})


@custom_login_required
def create_order(request):
    if request.method == 'POST':
        try:
            amount: int = int(request.POST.get("amount")) 
            print("Amount received: ", amount)

            if not amount or amount <= 0:
                return JsonResponse({"error": "Invalid amount provided."})

            order_data = {
                "amount": amount,
                "currency": "INR",
                "payment_capture": True
            }

            for _ in range(3):  # Retry 3 times if rate limit error occurs
                try:
                    order_response = client.order.create(order_data)
                    print("Order response: ", order_response)
                    break
                except razorpay.errors.RazorpayError as e:
                    print("Error creating order: ", str(e))

            if 'id' not in order_response:
                return JsonResponse({"error": "Failed to create Razorpay order."})

            # Create Order
            order = Order.objects.create(
                user=request.user,
                total_price=amount / 100,
                razorpay_order_id=order_response['id']
            )

            Payment.objects.create(
                user=request.user,
                order=order,
                amount=amount / 100,
                payment_method='Razorpay',
                status='Pending',
                transaction_id=order_response['id']
            )

            return JsonResponse({
                "order_id": order_response['id'],
                "key": settings.RAZORPAY_KEY_ID,
                "amount": amount,
                'order_id_db': order.id,
            })
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Invalid request"})


@custom_login_required
def verify_payment(request):
    if request.method == "POST":
        try:
            data = request.POST
            print("Received Data: ", data)

            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")

            if not (razorpay_order_id and razorpay_payment_id and razorpay_signature):
                return JsonResponse({"error": "Missing required payment details."})

            # 1. Verify the Razorpay signature
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }

            client.utility.verify_payment_signature(params_dict)
            print("✅ Payment verification successful!")

            # 2. Mark payment and order as complete
            payment = Payment.objects.get(transaction_id=razorpay_order_id)
            payment.status = 'Completed'
            payment.is_paid = True
            payment.save()

            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.status = 'Completed'
            order.save()

            # Inside the try block and within transaction.atomic():

            with transaction.atomic():
                if request.user.is_authenticated:
                    # 1. Cart-based purchase
                    active_cart_items = Cart.objects.filter(user=request.user, is_active=True)

                    if active_cart_items.exists():
                        for cart_item in active_cart_items:
                            book = cart_item.book
                            quantity = cart_item.quantity

                            if book.stock >= quantity:
                                book.stock -= quantity
                                book.save()
                            else:
                                return JsonResponse({
                                    "error": f"Insufficient stock for book: {book.title}"
                                })

                        active_cart_items.delete()
                        print("🧹 Purchased items deleted from cart!")

                    # 2. Direct purchase (book_id sent via POST)
                    else:
                        book_id = request.POST.get("book_id")
                        category_id = request.POST.get("category_id")
                        quantity = int(request.POST.get("quantity", 1))

                        if book_id and category_id:
                            book = get_object_or_404(Book, id=book_id, category_id=category_id)

                            if book.stock >= quantity:
                                book.stock -= quantity
                                book.save()
                                print(f"📦 Direct purchase: stock updated for {book.title}")
                            else:
                                return JsonResponse({
                                    "error": f"Insufficient stock for book: {book.title}"
                                })
                        else:
                            return JsonResponse({"error": "Missing book info for direct purchase."})


            return JsonResponse({
                "success": True,
                "message": "Payment verified and all items processed.",
                "order_id": order.id
            })

        except razorpay.errors.SignatureVerificationError:
            print("❌ Signature verification failed!")
            return JsonResponse({"error": "Invalid payment signature."})

        except Exception as e:
            print("⚠️ Error:", str(e))
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method"})
