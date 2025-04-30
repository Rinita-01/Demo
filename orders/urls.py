from django.urls import path
from .views import order_form, order_list, download_order_pdf, payment,order_form_cart

urlpatterns = [
    path('payment/', payment, name='payment'),
    path('order_form/<int:book_id>/<int:category_id>/', order_form, name='order_form'),
    path('order_pdf/<int:order_id>/', download_order_pdf, name='download_order_pdf'),
    path('order_list/', order_list, name='order_list'), 
    path('order_form_cart/', order_form_cart, name='order_form_cart'),
]