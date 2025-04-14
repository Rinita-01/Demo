from django.shortcuts import render
from books.models import Book
from django.db.models import Avg

def show(request):
    books = Book.objects.all()
    books = Book.objects.order_by('-created_at')[:3]
    books = Book.objects.all().annotate(average_rating=Avg('review__rating'))
    return render(request, "home/index.html", {'books': books })