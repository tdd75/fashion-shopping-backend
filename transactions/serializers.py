from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Transaction


class TransactionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionDetailSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Transaction
        exclude = ('product',)
