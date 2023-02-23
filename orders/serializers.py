from typing import List
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from django.utils import timezone

from api.serializers import OwnedPrimaryKeyRelatedField
from cart.models import CartItem
from cart.serializers import CartItemSerializer
from addresses.models import Address
from addresses.serializers import AddressSerializer
from discount_tickets.models import DiscountTicket
from discount_tickets.serializers import DiscountTicketSerializer
from transactions.serializers import TransactionSerializer
from custom_users.serializers import UserSerializer
from .models import Order


class OrderSerializer(FlexFieldsModelSerializer):
    order_items = OwnedPrimaryKeyRelatedField(
        queryset=CartItem.objects.is_ordered(False), source='cartitem_set', many=True)
    address = OwnedPrimaryKeyRelatedField(
        queryset=Address.objects.all())
    discount_ticket = serializers.PrimaryKeyRelatedField(
        queryset=DiscountTicket.objects.all(), required=False, allow_null=True)
    discount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    paid_at = serializers.DateTimeField(read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    expandable_fields = {
        'order_items': (CartItemSerializer, {'source': 'cartitem_set', 'many': True}),
        'address': AddressSerializer,
        'discount_ticket': DiscountTicketSerializer,
    }

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('code', 'order_items', 'stage')

    def validate_discount_ticket(self, value):
        if hasattr(value, 'ticketuserrel_set'):
            ticket_rel = value.ticketuserrel_set.filter(
                user_id=self.context['request'].user.id).first()
            if not ticket_rel:
                raise serializers.ValidationError(
                    'You do not have this ticket')
            if ticket_rel.is_active == False:
                raise serializers.ValidationError('You used this ticket')
            if value.end_at < timezone.now():
                raise serializers.ValidationError('This ticket is expired')

        return value


class OrderAdminSerializer(FlexFieldsModelSerializer):
    order_items = OwnedPrimaryKeyRelatedField(
        queryset=CartItem.objects.is_ordered(False), source='cartitem_set', many=True)
    address = OwnedPrimaryKeyRelatedField(
        queryset=Address.objects.all())
    discount_ticket = serializers.PrimaryKeyRelatedField(
        queryset=DiscountTicket.objects.all(), required=False, allow_null=True)
    discount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    paid_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    expandable_fields = {
        'order_items': (CartItemSerializer, {'source': 'cartitem_set', 'many': True}),
        'address': AddressSerializer,
        'discount_ticket': DiscountTicketSerializer,
        'owner': UserSerializer,
        'transaction': TransactionSerializer,
    }
