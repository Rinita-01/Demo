from django.urls import path
from .views import CartListCreateView, CartDetailView, show_cart, add_to_cart, update_cart, remove_from_cart

urlpatterns = [
    path('show_cart/', show_cart, name='show_cart'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path("update/", update_cart, name="update_cart"),
    path("remove/", remove_from_cart, name="remove_cart"),


    path('cart/', CartListCreateView.as_view(), name='cart-list-create'),
    path('cart/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
]