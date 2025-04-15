from django.shortcuts import render, get_object_or_404
import razorpay
import time
import requests.exceptions
from django.http import JsonResponse

from buybook import settings
from orders.models import Order
from .models import Payment
from books.models import Book
from orderitem.models import OrderItem
from users.decoraters import custom_login_required
from django.db.models import F

# Razorpay client initialization
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def payment(request):
    amount = request.POST.get("amount")
    return render(request, "payments/payment.html", {"amount": amount})

@custom_login_required
def order_success(request , order_id):
    order = get_object_or_404(Order, id=order_id )
    return render(request, 'orders/order_success.html', {'order': order})

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

def verify_payment(request):
    if request.method == "POST":
        try:
            data = request.POST
            print("Received Data: ", data)
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")

            book_id = request.POST.get("book_id")
            category_id = request.POST.get("category_id")
            quantity = int(request.POST.get("quantity", 1))

            # Reduce stock
            book = get_object_or_404(Book, id=book_id, category_id=category_id)
            book.stock -= quantity
            book.save()

            print("Payment-Book ID: ", book_id)
            print("Payment-Category ID: ", category_id)
            print("Payment-Quantity: ", quantity)

            if not (razorpay_order_id and razorpay_payment_id and razorpay_signature):
                return JsonResponse({"error": "Missing required payment details."})

            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }

            try:
                client.utility.verify_payment_signature(params_dict)
                print("Payment verification successful!")

                payment = Payment.objects.get(transaction_id=razorpay_order_id)
                payment.status = 'Completed'
                payment.is_paid = True
                payment.save()

                order = Order.objects.get(razorpay_order_id=razorpay_order_id)
                order.status = 'Completed'
                order.save()

            except razorpay.errors.SignatureVerificationError:
                print("Signature verification failed!")
                return JsonResponse({"error": "Invalid payment signature."})

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Invalid request method"})