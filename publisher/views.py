from django.shortcuts import render
from .models import Publisher
from rest_framework import generics
from .serializers import PublisherSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .models import Publisher
from .serializers import PublisherSerializer

def show_publisher(request):
    publishers = Publisher.objects.all()
    return render(request, 'publishers/publisher.html', {'publishers':publishers})


class PublisherListCreation(generics.ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def create(self, request, *args, **kwargs):
        # Call the original create method
        response = super().create(request, *args, **kwargs)
        
        # Return a custom response after creation
        return Response({
            'message': 'Publisher created successfully!',
            'data': response.data
        }, status=status.HTTP_201_CREATED)
    
    # Optional: Customize the response for GET (list) request
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'message': 'Publisher list fetched successfully!',
            'data': response.data
        }, status=status.HTTP_200_OK)


class PublisherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            'message': 'Publisher details fetched successfully!',
            'data': response.data
        }, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'message': 'Publisher updated successfully!',
            'data': response.data
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response({
            'message': 'Publisher deleted successfully!',
            'data': None  # No data returned after deletion
        }, status=status.HTTP_204_NO_CONTENT)
