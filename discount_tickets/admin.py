from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from discount_tickets.models import DiscountTicket


class DiscountTicketAdminForm(ModelForm):
    def clean_start_at(self):
        start_at = self.cleaned_data.get('start_at')
        if start_at and start_at > timezone.now():
            raise ValidationError('Start date must be in the future.')
        return start_at

    def clean(self):
        cleaned_data = super().clean()
        end_at = cleaned_data.get('end_at')
        start_at = cleaned_data.get('start_at')
        if start_at and end_at and end_at < start_at:
            raise ValidationError('End date must be after start date.')
        return cleaned_data

    class Meta:
        model = DiscountTicket
        exclude = ('saved_users',)


@admin.register(DiscountTicket)
class DiscountTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'percent', 'min_amount', 'start_at', 'end_at')
    ordering = ('id',)
    form = DiscountTicketAdminForm
