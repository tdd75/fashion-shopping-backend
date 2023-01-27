from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from datetime import datetime

from .models import Order
from cart.models import CartItem
from cart.serializers import CartItemSerializer
from addresses.models import Address
from addresses.serializers import AddressSerializer
from discount_tickets.models import DiscountTicket
from discount_tickets.serializers import DiscountTicketSerializer
from api.serializers import OwnerFilteredPrimaryKeyRelatedField


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

    def save(self, **kwargs):
        # TODO: Implement backup data logic for order
        # data = self.validated_data
        # backup_data = {}

        # def omit_state_dict(data):
        #     data.pop('_state', None)
        #     return data

        # for field in ['discount_ticket', 'owner']:
        #     if data.get(field):
        #         backup_data[field] = omit_state_dict(data[field].__dict__)
        # if data.get('order_items'):
        #     backup_data['order_items'] = [
        #         omit_state_dict(cart_item.__dict__) for cart_item in data['order_items']]

        # if backup_data:
        #     kwargs['backup_data'] = backup_data
        # kwargs['backup_data'] = {
        #     'id': 1,
        #     'address': {
        #         'city': 'Hanoi'
        #     },
        # }
        return super().save(**kwargs)
