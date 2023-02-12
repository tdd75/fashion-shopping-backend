from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from drf_extra_fields.fields import Base64ImageField

from .models import Product
from product_variants.serializers import ProductVariantSerializer
from product_categories.serializers import ProductCategorySerializer


class ProductSerializer(FlexFieldsModelSerializer):
    image = Base64ImageField()
    price_range = serializers.ListField(child=serializers.DecimalField(
        max_digits=12, decimal_places=2), read_only=True)
    stocks = serializers.IntegerField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    is_favorite = serializers.SerializerMethodField()

    expandable_fields = {
        'variants': (ProductVariantSerializer, {'many': True, 'source': 'productvariant_set'})
    }

    class Meta:
        model = Product
        exclude = ('favorited_users', 'feature_vector')

    def get_is_favorite(self, obj) -> bool:
        return obj.favorited_users.filter(id=self.context['request'].user.id).exists()


class ProductFavoriteSerializer(serializers.Serializer):
    is_favorite = serializers.BooleanField()


class ProductImageSearchSerializer(serializers.Serializer):
    image = Base64ImageField()


class ProductFilterSerializer(serializers.Serializer):
    price_range = serializers.ListField(
        child=serializers.DecimalField(decimal_places=2, max_digits=12))
    colors = serializers.ListField(child=serializers.CharField())
    sizes = serializers.ListField(child=serializers.CharField())
    categories = serializers.ListField(child=ProductCategorySerializer())


class ProductAdminSerializer(FlexFieldsModelSerializer):
    image = Base64ImageField()
    price_range = serializers.ListField(child=serializers.DecimalField(
        max_digits=12, decimal_places=2), read_only=True)
    stocks = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(
        max_digits=2, decimal_places=1, read_only=True)

    expandable_fields = {
        'variants': (ProductVariantSerializer, {'many': True, 'source': 'productvariant_set'}),
        'category': ('product_categories.serializers.ProductCategorySerializer', {'source': 'category'})
    }

    class Meta:
        model = Product
        exclude = ('favorited_users',)
