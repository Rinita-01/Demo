from rest_framework import serializers
from .models import Publisher

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher  # <-- model, not models
        fields = ['id', 'name', 'address', 'contact', 'website']
