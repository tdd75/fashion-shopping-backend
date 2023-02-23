from django.contrib import admin

from .models import CartItem

from orders.models import Order


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_variant',
                    'product_variant__product', 'quantity', 'order', 'owner')
    list_filter = ('owner',)

    def product_variant__product(self, obj):
        return obj.product_variant.product
