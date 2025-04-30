from django.urls import path
from .views import create_order, payment, verify_payment, order_success

urlpatterns = [
    path('create_order/', create_order, name='create_order'),
    path('payment/', payment, name='payment'),
    path('verify_payment/', verify_payment, name='verify_payment'),
    path('order_success/<int:order_id>/', order_success, name='order_success'),
]