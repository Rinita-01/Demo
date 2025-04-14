from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book
from orders.models import Order
from users.decoraters import custom_login_required
from django.core.paginator import Paginator
from rest_framework import generics
from .serializers import BookSerializer
from django.db.models import Avg

def show_books(request):
    books = Book.objects.all()
    books = Book.objects.all().annotate(average_rating=Avg('review__rating'))
    paginator = Paginator(books, 3)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "books/books.html", {"page_obj": page_obj,'books': books})


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Retrieve, Update, and Delete View
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

