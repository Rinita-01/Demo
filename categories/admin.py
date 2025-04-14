from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Show category ID and name
    search_fields = ('name',)  # Enable search by name
    ordering = ('name',)  # Sort alphabetically
