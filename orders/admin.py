from django.contrib import admin

from .models import Order

from cart.models import CartItem


class OrderItemInline(admin.TabularInline):
    model = CartItem
    fields = ('product_variant', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'stage', 'amount',
                    'payment_method', 'created_at')
    inlines = (OrderItemInline,)
    ordering = ('-id',)
    actions = ('set_quantity_zero',)
    list_filter = ('stage',)
    search_fields = ('name', 'description')
