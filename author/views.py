from django.shortcuts import render
from .models import Author
from rest_framework import generics
from .serializers import AuthorSerializer

def show_author(request):
    authors = Author.objects.all()

    
    return render(request, 'author/author.html', {'authors': authors}) 







class AuthorListCreation(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


