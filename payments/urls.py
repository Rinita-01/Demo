from django.urls import path
from .views import create_order, payment, verify_payment, order_success

urlpatterns = [
    path('create_order/', create_order, name='create_order'),
    path('payment/', payment, name='payment'),
    path('verify_payment/', verify_payment, name='verify_payment'),
    path('order_success/<int:order_id>/', order_success, name='order_success'),
    # path('send_order_confirmation_email_with_pdf/<int:order_id>/', send_book_pdf_email, name='send_order_confirmation_email_with_pdf')
]