from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from drf_extra_fields.fields import Base64ImageField

from .models import Product
from product_types.serializers import ProductTypeSerializer


class ProductSerializer(FlexFieldsModelSerializer):
    image = Base64ImageField()
    price_range = serializers.ListField(child=serializers.DecimalField(
        max_digits=12, decimal_places=2), read_only=True)
    stocks = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(
        max_digits=2, decimal_places=1, read_only=True)
    is_favorite = serializers.SerializerMethodField()

    expandable_fields = {
        'product_types': (ProductTypeSerializer, {'many': True, 'source': 'producttype_set'})
    }

    class Meta:
        model = Product
        exclude = ('favorited_users',)

    def get_is_favorite(self, obj) -> bool:
        return obj.favorited_users.filter(id=self.context['request'].user.id).exists()


class ProductFavoriteSerializer(serializers.Serializer):
    is_favorite = serializers.BooleanField()
