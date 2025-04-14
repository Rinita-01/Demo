from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Returns username instead of ID
    book = serializers.StringRelatedField()  # Returns book title instead of ID

    class Meta:
        model = Cart
        fields = ['id', 'user', 'book', 'quantity', 'added_at']
