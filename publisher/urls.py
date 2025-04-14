from django.urls import path
from .views import PublisherListCreation, PublisherDetailView, show_publisher

urlpatterns = [
    path('show_publishers/', show_publisher, name='show_publishers'),
    path('publishers/', PublisherListCreation.as_view(), name='publisher-list-create'),
    path('publishers/<int:pk>', PublisherDetailView.as_view(), name='publisher-details')
]