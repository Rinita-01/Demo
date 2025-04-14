from django.db.models import Sum, F, DecimalField
from decimal import Decimal
from cart.models import Cart

def cart_context(request):
    """Context processor to provide cart details across all templates."""
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_items = cart_items.count()

        if cart_items.exists():
            shipping_amount = Decimal("70.00")  # Ensure decimal consistency

            # Use `output_field=DecimalField()` to prevent Decimal type errors
            amount = cart_items.aggregate(
                total=Sum(F('quantity') * F('book__price'), output_field=DecimalField(max_digits=10, decimal_places=2))
            )['total'] or Decimal("0.00")

            total_amount = amount + shipping_amount
        else:
            amount = Decimal("0.00")
            total_amount = Decimal("0.00")

        return {
            'cart_items': cart_items,
            'total_items': total_items,
            'cart_amount': amount,
            'cart_total_amount': total_amount,
        }

    return {
        'cart_items': [],
        'total_items': 0,
        'cart_amount': Decimal("0.00"),
        'cart_total_amount': Decimal("0.00"),
    }
