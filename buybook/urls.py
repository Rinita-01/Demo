from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('users.urls')),
    path('category/', include('categories.urls')), 
    path('author/', include('author.urls')),
    path('publisher/', include('publisher.urls')), 
    path('book/', include('books.urls')),  
    path('order/', include('orders.urls')),
    path('cart/', include('cart.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('', views.show, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

