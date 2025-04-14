from django.shortcuts import render
from .models import Publisher
from rest_framework import generics
from .serializers import PublisherSerializer

def show_publisher(request):
    publishers = Publisher.objects.all()
    return render(request, 'publishers/publisher.html', {'publishers':publishers})

class PublisherListCreation(generics.ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class PublisherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer