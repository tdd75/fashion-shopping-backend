from django.contrib import admin

from .models import ProductVariant


@admin.register(ProductVariant)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'size', 'stocks','price')
    ordering = ('-created_at',)
    search_fields = ('color', 'size')
