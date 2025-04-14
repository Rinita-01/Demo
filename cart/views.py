from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField
from books.models import Book
from cart.models import Cart
import logging
from decimal import Decimal
from django.http import JsonResponse
from decimal import Decimal
from django.db.models import Sum, F, DecimalField
from .models import Cart, Book
from users.decoraters import custom_login_required

logger = logging.getLogger(__name__)

def payment(request):
    amount = request.POST.get('amount')
    return render(request, 'payments/payment.html', {'amount': amount})

@custom_login_required
def add_to_cart(request):
    if request.method == "POST":
        try:
            book_id = request.POST.get('prod_id')
            logger.info(f"Received book_id: {book_id}")

            if not book_id:
                return JsonResponse({"status": "error", "message": "Book ID missing!"}, status=400)

            book = get_object_or_404(Book, id=book_id)

            # Ensure stock is available
            if book.stock <= 0:
                return JsonResponse({"status": "error", "message": "This book is out of stock!"}, status=400)

            # Add or update cart item
            cart_item, created = Cart.objects.get_or_create(user=request.user, book=book) 
            print(f"Cart item created: {cart_item}, Created: {created}")
            print(f"Initial Quantity: {cart_item.quantity}")
            if not created:
                cart_item.quantity += 1
                cart_item.save()

                # cart_item = Cart.objects.filter(user=request.user, book=book_id).first()
                # if cart_item:
                #     print(f"Quantity: {cart_item.quantity}")
                # else:
                #     print("Book not in cart for this user.")
                # print(f'No. of items in cart: {Cart.objects.filter(user=request.user).count()}')
                
            cart_items = Cart.objects.filter(user=request.user)
            total_items = cart_items.count()
            print(f"No. of cart items: {total_items}")
            return JsonResponse({"status": "success", "message": f"{book.title} added to cart!", "total_item": total_items})
        except Exception as e:
            logger.error(f"Error in add_to_cart: {e}")
            return JsonResponse({"status": "error", "message": "Something went wrong!"}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request!"}, status=400)

@custom_login_required
def show_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_item_count = cart_items.count()

    if cart_items.exists():
        shipping_amount = Decimal("70.00")  # Fixed shipping cost as Decimal

        # Calculate total amount using F expressions for better performance
        amount = cart_items.aggregate(
            total=Sum(F('quantity') * F('book__price'), output_field=DecimalField())
        )['total'] or Decimal("0.00")

        total_amount = amount + shipping_amount  # Ensure both are Decimal

        context = {
            'carts': cart_items,
            'amount': amount.quantize(Decimal("0.00")),  # Format to 2 decimal places
            'total_amount': total_amount.quantize(Decimal("0.00")),
            'total_item': total_item_count
        }
        return render(request, 'cart/add_to_cart.html', context)

    return render(request, 'cart/empty_cart.html', {'total_item': total_item_count})

@custom_login_required
def update_cart(request):
    if request.method == "GET":
        book_id = request.GET.get("book_id")
        action = request.GET.get("action")

        cart_item = Cart.objects.get(user=request.user, book_id=book_id)

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                return JsonResponse({"success": True, "quantity": 0, "amount": 0, "total_amount": 0})

        cart_item.save()

        # Recalculate totals
        cart_items = Cart.objects.filter(user=request.user)
        shipping_amount = Decimal("70.00")
        amount = cart_items.aggregate(
            total=Sum(F("quantity") * F("book__price"), output_field=DecimalField())
        )["total"] or Decimal("0.00")

        total_amount = amount + shipping_amount

        return JsonResponse({
            "success": True,
            "quantity": cart_item.quantity,
            "amount": float(amount),  # Convert to float
            "total_amount": float(total_amount)  # Convert to float
        })

    return JsonResponse({"success": False})

@custom_login_required
def remove_from_cart(request):
    if request.method == "GET":
        book_id = request.GET.get("book_id")
        cart_item = get_object_or_404(Cart, book__id=book_id, user=request.user)
        cart_item.delete()

        # Recalculate totals after removal
        amount = sum(item.book.price * item.quantity for item in Cart.objects.filter(user=request.user))
        total_amount = amount + 70

        return JsonResponse({"success": True, "amount": amount, "total_amount": total_amount})

    return JsonResponse({"success": False})







from rest_framework import generics
from .models import Cart
from .serializers import CartSerializer

# List and Create Cart Items
class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

# Retrieve, Update, and Delete Cart Items
class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
