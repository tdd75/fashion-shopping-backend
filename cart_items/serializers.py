from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    amount = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        exclude = ('order', 'owner')
        read_only_fields = ('rating', 'size', 'color',
                            'image', 'price')
        optional_fields = ('product_type',)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data['quantity'] > validated_data['product_type'].quantity:
            raise ValidationError({
                'quantity': f'Products quantity exceeds the available quantity \
                    ({validated_data["product_type"].quantity})'
            })

        return validated_data

    def create(self, validated_data):
        # backup product information
        product_type = validated_data.get('product_type')
        for fields in ['size', 'color', 'price']:
            validated_data[fields] = getattr(product_type, fields)
        validated_data['image'] = getattr(product_type.product, 'image')

        return super().create(validated_data)
