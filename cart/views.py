from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField
from books.models import Book
from cart.models import Cart
import logging
from decimal import Decimal
from django.http import JsonResponse
from decimal import Decimal
from django.db.models import Sum, F, DecimalField
from users.decoraters import custom_login_required

logger = logging.getLogger(__name__)

def payment(request):
    if request.method == "POST":
        amount = request.POST.get("amount", "0.00")
        book_id = request.POST.get("book_id")
        category_id = request.POST.get("category_id")
        
        try:
            quantity = int(request.POST.get("quantity") or 1)
        except ValueError:
            quantity = 1

        return render(request, "payments/payment.html", {
            "amount": amount,
            "book_id": book_id,
            "category_id": category_id,
            "quantity": quantity
        })
    else:
        return redirect('show_cart')  # safer fallback than rendering

# @require_POST
@custom_login_required
def add_to_cart(request):
    try:
        book_id = request.POST.get('prod_id')
        if not book_id:
            return JsonResponse({"status": "error", "message": "Book ID missing!"}, status=400)

        book = get_object_or_404(Book, id=book_id)
        print(f"Book ID: {book_id}, Book Title: {book.title}")

        # Ensure stock is available
        if book.stock <= 0:
            return JsonResponse({"status": "error", "message": "This book is out of stock!"}, status=400)

        # Add or update cart item only if active
        cart_item, created = Cart.objects.get_or_create(user=request.user, book=book,is_active=True)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        total_items = Cart.objects.filter(user=request.user, is_active=True).count()

        return JsonResponse({
            "status": "success",
            "message": f"{book.title} added to cart!",
            "total_item": total_items
        })

    except Exception as e:
        logger.error(f"Error in add_to_cart: {e}")
        return JsonResponse({"status": "error", "message": "Something went wrong!"}, status=500)


@custom_login_required
def show_cart(request):
    all_cart_items = Cart.objects.filter(user=request.user)
    active_cart_items = all_cart_items.filter(is_active=True)
    total_item_count = all_cart_items.count()
    print(f"Total Items in Cart: {total_item_count}")

    if all_cart_items.exists():
        # Calculate amount only from active items
        amount = active_cart_items.aggregate(
            total=Sum(F('quantity') * F('book__price'), output_field=DecimalField())
        )['total'] or Decimal("0.00")

        shipping_amount = Decimal("70.00") if amount > 0 else Decimal("0.00")
        total_amount = amount + shipping_amount

        context = {
            'carts': all_cart_items,  # still show all items
            'amount': amount.quantize(Decimal("0.00")),
            'total_amount': total_amount.quantize(Decimal("0.00")),
            'total_item': total_item_count
        }
        return render(request, 'cart/add_to_cart.html', context)

    return render(request, 'cart/empty_cart.html', {'total_item': total_item_count})

# This view is called  via AJAX when oggle_cart_item is called
@custom_login_required
def cart_totals(request):
    if request.user.is_authenticated:
        active_items = Cart.objects.filter(user=request.user, is_active=True)

        amount = active_items.aggregate(
            total=Sum(F('quantity') * F('book__price'), output_field=DecimalField())
        )['total'] or Decimal("0.00")

        shipping_amount = Decimal("70.00") if amount > 0 else Decimal("0.00")
        total_amount = amount + shipping_amount

        return JsonResponse({
            'amount': f"{amount:.2f}",
            'shipping': f"{shipping_amount:.2f}",
            'total_amount': f"{total_amount:.2f}"
        })
    return JsonResponse({'error': 'Unauthorized'}, status=401)

# This view is called via AJAX when the user toggles the cart item via the checkbox
@custom_login_required
@require_POST
def toggle_cart_item(request):
    cart_id = request.POST.get('cart_id')
    is_active = request.POST.get('is_active') == 'true'  # string to boolean

    try:
        cart = Cart.objects.get(id=cart_id, user=request.user)
        cart.is_active = is_active
        cart.save()

        # Calculate total items after update
        total_items = Cart.objects.filter(user=request.user, is_active=True).count()

        return JsonResponse({'status': 'success', 'message': f'Cart item {cart_id} updated.'})
    except Cart.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cart item not found.'}, status=404)

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
