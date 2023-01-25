from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_flex_fields import FlexFieldsModelSerializer

from .models import CartItem
from product_types.serializers import ProductTypeSerializer


class CartItemSerializer(FlexFieldsModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    expandable_fields = {
        'product_type': ProductTypeSerializer,
    }

    class Meta:
        model = CartItem
        fields = '__all__'

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        stocks = self.instance.product_type.stocks if self.instance \
            else validated_data['product_type'].stocks
        if validated_data['quantity'] > stocks:
            raise ValidationError({
                'quantity': f'The quantity exceeds the available stocks ({stocks})'
            })
        return validated_data
