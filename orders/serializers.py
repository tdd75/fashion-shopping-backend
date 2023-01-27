from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Order
from cart.models import CartItem
from cart.serializers import CartItemSerializer
from addresses.models import Address
from addresses.serializers import AddressSerializer
from api.serializers import ManyToManyUpdateField, ManyToManyUpdateFieldsMixin


class OrderSerializer(ManyToManyUpdateFieldsMixin, FlexFieldsModelSerializer):
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    cart_items = ManyToManyUpdateField(source='cartitem_set')
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    expandable_fields = {
        'cart_items': (CartItemSerializer, {'many': True, 'source': 'cartitem_set'}),
        'address': AddressSerializer,
    }

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'code', 'order_items')
