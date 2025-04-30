from django.urls import path
from .views import show_cart, add_to_cart, update_cart, remove_from_cart,payment, cart_totals,toggle_cart_item

urlpatterns = [
    path('show_cart/', show_cart, name='show_cart'),
    path('toggle-cart-item/', toggle_cart_item, name='toggle_cart_item'),
    path("totals/", cart_totals, name="cart_totals"),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path("update/", update_cart, name="update_cart"),
    path("remove/", remove_from_cart, name="remove_cart"),
    path('payment/', payment, name='payment'),
]