import datetime
from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import DiscountTicket


class DiscountTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountTicket
        fields = '__all__'

    def validate(self, attrs):
        if attrs['start_date'].date() < datetime.date.today():
            raise ValidationError("Start date cannot be in the past!")
        if attrs['start_date'] > attrs['end_date']:
            raise ValidationError("End date cannot be before start date!")
        if attrs['type'] == DiscountTicket.DiscountType.RAW_VALUE and attrs['min_amount'] < attrs['value']:
            raise ValidationError(
                "Minimum order amount cannot be less than discount value!")

        return attrs
