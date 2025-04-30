from django.urls import path
from .views import (RegisterAPIView, LoginAPIView, UserAPIView, RefreshAPIView, LogoutAPIView, 
customer_registration, admin_registration, customer_login, myAccount, logout, activate, 
order_list, AdminRegistrationAPIView, AdminLoginAPIView)

urlpatterns = [
    path('register/', customer_registration, name='customer_registration'),
    path('customer_login/', customer_login, name='customer_login'),
    path('myAccount/', myAccount, name='myAccount'),
    path('logout/', logout, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('admin_registration/', admin_registration, name='admin_registration'),
    path('order_list/', order_list, name='order_list'),  # New URL pattern for order list

    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('refresh/', RefreshAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('api/admin-register/', AdminRegistrationAPIView.as_view(), name='api_admin_registration'),
    path('api/admin-login/', AdminLoginAPIView.as_view(), name='api_admin_login')

]
