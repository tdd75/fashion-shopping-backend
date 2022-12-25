from rest_framework import serializers

from .models import Order
from cart_items.models import CartItem
from cart_items.serializers import CartItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(source='cartitem_set', many=True)
    amount = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'code')


class OrderCreateSerializer(serializers.ModelSerializer):
    cart_items = serializers.PrimaryKeyRelatedField(
        queryset=CartItem.objects.all(), many=True, write_only=True)
    amount = serializers.ReadOnlyField()

    Meta = OrderSerializer.Meta

    def create(self, validated_data):
        cartitem_set = validated_data.pop('cart_items')
        instance = super().create(validated_data)
        instance.cartitem_set.add(*cartitem_set)
        return instance
