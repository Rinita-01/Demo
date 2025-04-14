from django.contrib import admin
from django.utils.html import format_html
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'category', 'price', 'stock', 'cover_preview', 'pdf_link', 'created_at')
    search_fields = ('title', 'author__name', 'publisher__name', 'category__name')
    list_filter = ('author', 'publisher', 'category', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('cover_preview', 'pdf_link')

    def cover_preview(self, obj):
        """Display a small preview of the book cover image."""
        if obj.cover_image:
            return format_html('<img src="{}" width="50" style="border-radius:5px;">', obj.cover_image.url)
        return "No Image"

    cover_preview.allow_tags = True
    cover_preview.short_description = "Cover Preview"

    def pdf_link(self, obj):
        """Provide a clickable link to the uploaded PDF file."""
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.pdf_file.url)
        return "No PDF"

    pdf_link.allow_tags = True
    pdf_link.short_description = "PDF File"
