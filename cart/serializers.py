from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_flex_fields import FlexFieldsModelSerializer

from .models import CartItem
from product_variants.models import ProductVariant
from product_variants.serializers import ProductVariantSerializer


class CartItemSerializer(FlexFieldsModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_variant = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all())
    is_reviewed = serializers.SerializerMethodField()

    expandable_fields = {
        'product_variant': ProductVariantSerializer,
    }

    class Meta:
        model = CartItem
        fields = '__all__'

    def validate(self, attrs):
        stocks = self.instance.product_variant.stocks if self.instance \
            else attrs['product_variant'].stocks
        if attrs['quantity'] > stocks:
            raise ValidationError({
                'quantity': f'The quantity exceeds the available stocks ({stocks})'
            })
        return super().validate(attrs)

    def get_is_reviewed(self, obj) -> bool:
        try:
            return obj.order.review_set.has_owned(self.context['request'].user.id).exists()
        except:
            return False
