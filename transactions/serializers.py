from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from orders.models import Order

from .models import Transaction


class TransactionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Transaction
        fields = ('payment_link', 'order')
        write_only_fields = ('order',)
        read_only_fields = ('payment_link',)

    def validate_order(self, value):
        if value.payment_method == Order.PaymentMethod.COD:
            raise serializers.ValidationError(
                'You can not create for COD order')
        return value
