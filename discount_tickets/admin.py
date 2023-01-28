from django.contrib import admin
from django.forms import ModelForm
from discount_tickets.models import DiscountTicket


class DiscountTicketAdminForm(ModelForm):
    class Meta:
        model = DiscountTicket
        exclude = ('saved_users',)


class DiscountTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'percent', 'min_amount', 'start_at', 'end_at')
    ordering = ('id',)
    form = DiscountTicketAdminForm


admin.site.register(DiscountTicket, DiscountTicketAdmin)
