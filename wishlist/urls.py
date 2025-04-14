from django.urls import path
from .views import add_to_wishlist, show_wishlist, remove_from_wishlist

urlpatterns = [ 
     path('add-to-wishlist/<int:book_id>/', add_to_wishlist, name='add_to_wishlist'),
     path('wishlist/', show_wishlist, name='show_wishlist'),
     path('remove-from-wishlist/<int:book_id>/', remove_from_wishlist, name='remove_from_wishlist' ),
]