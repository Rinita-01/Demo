from django.contrib import admin
from .models import Publisher

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'website')  # Show publisher name, contact, and website
    search_fields = ('name', 'contact')  # Enable search by name and contact
    list_filter = ('name',)  # Add filtering by name
    ordering = ('name',)  # Sort publishers alphabetically
