from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ('product',)
