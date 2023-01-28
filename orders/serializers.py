from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from datetime import datetime

from api.serializers import OwnerFilteredPrimaryKeyRelatedField
from cart.models import CartItem
from cart.serializers import CartItemSerializer
from addresses.models import Address
from addresses.serializers import AddressSerializer
from discount_tickets.models import DiscountTicket
from discount_tickets.serializers import DiscountTicketSerializer
from .models import Order


class OrderSerializer(FlexFieldsModelSerializer):
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_items = OwnerFilteredPrimaryKeyRelatedField(
        queryset=CartItem.objects, source='order_items', many=True)
    address = OwnerFilteredPrimaryKeyRelatedField(
        queryset=Address.objects)
    discount_ticket = serializers.PrimaryKeyRelatedField(
        queryset=DiscountTicket.objects.all(), required=False)

    expandable_fields = {
        'cart_items': (CartItemSerializer, {'many': True, 'source': 'order_items'}),
        'address': AddressSerializer,
        'discount_ticket': DiscountTicketSerializer,
    }

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('code', 'order_items')

    def validate_discount_ticket(self, value):
        ticket_rel = value.ticketuserrel_set.filter(
            user_id=self.context['request'].user.id).first()
        if not ticket_rel:
            raise serializers.ValidationError('You do not have this ticket')
        elif ticket_rel.is_active == False:
            raise serializers.ValidationError('You used this ticket')
        elif value.end_at < datetime.now():
            raise serializers.ValidationError('This ticket is expired')

        return value
