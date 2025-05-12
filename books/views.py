from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book
from orders.models import Order
from users.decoraters import custom_login_required
from django.core.paginator import Paginator
from rest_framework import generics
from .serializers import BookSerializer
from django.db.models import Avg
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics


def show_books(request):
    # books = Book.objects.all()
    books = Book.objects.all().annotate(average_rating=Avg('review__rating'))
    paginator = Paginator(books, 3)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "books/books.html", {"page_obj": page_obj})


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'message': 'Book list fetched successfully!',
            'data': response.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Book created successfully!',
            'data': response.data
        }, status=status.HTTP_201_CREATED)

# Retrieve, Update, and Delete View
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            'message': 'Book details fetched successfully!',
            'data': response.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'message': 'Book updated successfully!',
            'data': response.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response({
            'message': 'Book deleted successfully!',
            'data': None  # No data returned after deletion
        }, status=status.HTTP_204_NO_CONTENT)

