from django.contrib import admin
from django.utils.html import format_html
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'nationality', 'photo_preview')
    search_fields = ('name', 'nationality')
    list_filter = ('nationality', 'date_of_birth')
    ordering = ('name',)
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        """Display a small preview of the author's photo."""
        if obj.photo:
            return format_html('<img src="{}" width="50" style="border-radius:5px;">', obj.photo.url)
        return "No Image"

    photo_preview.allow_tags = True
    photo_preview.short_description = "Photo Preview"
