from django.urls import path
from .views import  show_author ,AuthorListCreation, AuthorDetailView

urlpatterns = [
    path('show_name/', show_author, name='show_name'),
    path('authors/', AuthorListCreation.as_view(), name='Author-list-create'),
    path('authors/<int:pk>', AuthorDetailView.as_view(), name='Author-detail'),
]