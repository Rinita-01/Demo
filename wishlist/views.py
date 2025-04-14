from django.shortcuts import redirect, get_object_or_404, render
from books.models import Book
from .models import Wishlist

def add_to_wishlist(request, book_id):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Login required'}, status=401)
        return redirect('login')

    book = get_object_or_404(Book, id=book_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, book=book)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'added': created})

    return redirect('show_wishlist')

def show_wishlist(request):
    if not request.user.is_authenticated:
        return redirect('login')  # redirect to login if user is not logged in

    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})

def remove_from_wishlist(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')  # redirect to login if user is not logged in

    book = get_object_or_404(Book, id=book_id)
    wishlist_item = get_object_or_404(Wishlist, user=request.user, book=book)
    wishlist_item.delete()

    return redirect('show_wishlist')  # adjust redirect as per your book detail view