from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_flex_fields import FlexFieldsModelSerializer

from .models import CartItem
from product_types.models import ProductType
from product_types.serializers import ProductTypeSerializer


class CartItemSerializer(FlexFieldsModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_type = serializers.PrimaryKeyRelatedField(
        queryset=ProductType.objects.all())

    expandable_fields = {
        'product_type': ProductTypeSerializer,
    }

    class Meta:
        model = CartItem
        fields = '__all__'

    def validate(self, attrs):
        stocks = self.instance.product_type.stocks if self.instance \
            else attrs['product_type'].stocks
        if attrs['quantity'] > stocks:
            raise ValidationError({
                'quantity': f'The quantity exceeds the available stocks ({stocks})'
            })
        return super().validate(attrs)
