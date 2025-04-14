from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Returns username instead of ID

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'created_at']
