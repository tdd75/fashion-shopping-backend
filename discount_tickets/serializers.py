from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from django.core.exceptions import ValidationError
import datetime

from .models import DiscountTicket


class DiscountTicketSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = DiscountTicket
        exclude = ('saved_users',)

    def validate(self, attrs):
        if attrs['start_date'].date() < datetime.date.today():
            raise ValidationError("Start date cannot be in the past!")
        if attrs['start_date'] > attrs['end_date']:
            raise ValidationError("End date cannot be before start date!")
        if attrs['type'] == DiscountTicket.DiscountType.RAW_VALUE and attrs['min_amount'] < attrs['value']:
            raise ValidationError(
                "Minimum order amount cannot be less than discount value!")

        return attrs
