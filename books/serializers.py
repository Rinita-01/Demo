from rest_framework import serializers
from .models import Book
from author.models import Author
from categories.models import Category
from publisher.models import Publisher

class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Returns author's name instead of ID
    publisher = serializers.StringRelatedField()  # Returns publisher's name instead of ID
    category = serializers.StringRelatedField()  # Returns category's name instead of ID

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'category', 'price', 'stock', 'description', 'cover_image','pdf_file', 'created_at']
