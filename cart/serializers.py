from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CartItem
from product_types.models import ProductType
from product_types.serializers import ProductTypeDetailSerializer


class CartItemSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    # request
    product_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductType.objects.all(), write_only=True)
    # response
    product_type = ProductTypeDetailSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CartItem
        exclude = ('order', 'owner', 'product')

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data['quantity'] > validated_data['product_type_id'].quantity:
            raise ValidationError({
                'quantity': f'Products quantity exceeds the available quantity \
                    ({validated_data["product_type_id"].quantity})'
            })
        return validated_data

    def create(self, validated_data):
        product_type = validated_data.pop('product_type_id')
        validated_data['product_type_id'] = product_type.id
        validated_data['product_id'] = product_type.product.id
        return super().create(validated_data)
