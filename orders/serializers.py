from rest_framework import serializers

from .models import Order
from cart.models import CartItem
from cart.serializers import CartItemSerializer
from addresses.models import Address
from addresses.serializers import AddressSerializer


class OrderSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    cart_items = CartItemSerializer(
        source='cartitem_set', many=True, read_only=True)
    cart_item_ids = serializers.PrimaryKeyRelatedField(
        queryset=CartItem.objects.all(), source='cartitem_set', many=True, write_only=True)
    # address = AddressSerializer(source='address', read_only=True)
    # address_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Address.objects.all(), source='address', write_only=True)

    class Meta:
        model = Order
        exclude = ('owner',)
        read_only_fields = ('created_at', 'updated_at', 'code', 'order_items')

    def create(self, validated_data):
        validated_data['owner_id'] = self.context['request'].user.id
        # address = validated_data.pop('address_id')
        # validated_data['address_id'] = address.id
        # for cart_item in cart_items.all():
        #     backup_fields = ['size', 'color', 'price']
    #     for field in backup_fields:
    #         validated_data[field] = getattr(product_type, field)
        instance = super().create(validated_data)
        return instance

    # def create(self, validated_data):
    #     # create backup product information
    #     product_type = validated_data.pop('cart_ids')
    #     backup_fields = ['size', 'color', 'price']
    #     for field in backup_fields:
    #         validated_data[field] = getattr(product_type, field)
    #     validated_data['image'] = product_type.product.image
    #     validated_data['product_type_id'] = product_type.id
    #     return super().create(validated_data)
