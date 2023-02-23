from django.contrib import admin
from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'paid_amount', 'paid_at')
    search_fields = ('order',)
