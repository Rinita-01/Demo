from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import Order
from users.decoraters import custom_login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from books.models import Book
from orders.models import Order
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from orderitem.models import OrderItem
from cart.models import Cart
from django.views.decorators.csrf import csrf_protect


@custom_login_required
@csrf_protect
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
        return render(request, "payments/payment.html", {"amount": "0.00"})

# This FBV will be called when the user clicks on the "Place Order" button for a book
@custom_login_required
def order_form(request, book_id, category_id):
    book = get_object_or_404(Book, id=book_id, category_id=category_id)
    quantity_range = range(1, book.stock + 1) if book.stock > 0 else range(1)

    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
            total_price = request.POST.get("total_price")

            if book.stock < quantity:
                return JsonResponse({"message": "Not enough stock available!"}, status=400)

            # If price not received from frontend
            if not total_price:
                total_price = book.price * quantity + 70 # Adding shipping cost
            else:
                total_price = float(total_price)            

            return JsonResponse({
                "status": "success",
                "message": "Stock updated successfully!",
                "total_price": total_price,
                "book_id": book.id,
                "category_id": category_id,
                "quantity": quantity
            })

        except Exception as e:
            return JsonResponse({"message": f"Error processing request: {str(e)}"}, status=400)

    context = {
        'book': book,
        'quantity_range': quantity_range
    }
    return render(request, 'orders/add_order.html', context)

# order from  cart
@custom_login_required
def order_form_cart(request):
    cart_items = Cart.objects.filter(user=request.user, is_active=True)
    total_item_count = cart_items.count()
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    total_price += 70 

    print("Total Price: ", total_price)
    print("Total Items in Cart: ", total_item_count)

    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
            total_price = request.POST.get("total_price")

            return JsonResponse({
                "status": "success",
                "message": "Stock updated successfully!",
                "total_price": total_price,
                "quantity": quantity
            })

        except Exception as e:
            return JsonResponse({"message": f"Error processing request: {str(e)}"}, status=400)

    return render(request, 'orders/add_order.html')

@custom_login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})    

@custom_login_required
def download_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    for item in items:
        item.total_price = item.quantity * item.price_at_purchase

    
    template_path = 'orders/order_pdf.html'
    context = {'order': order, 'items': items}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order_id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF: <pre>' + html + '</pre>')
    return response 



