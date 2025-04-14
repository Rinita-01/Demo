from rest_framework import serializers
from .models import Publisher

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        models = Publisher
        fields = ['id', 'name','address','contact','website']