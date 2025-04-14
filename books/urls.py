from django.urls import path
from .views import show_books, BookListCreateView, BookDetailView

urlpatterns = [
    path('show_books/' , show_books, name='show_books'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]