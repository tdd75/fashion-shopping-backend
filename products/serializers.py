from rest_framework import serializers

from .models import Product
from product_types.serializers import ProductTypeDetailSerializer


class ProductSerializer(serializers.ModelSerializer):
    product_types = ProductTypeDetailSerializer(
        source='producttype_set', many=True, required=False)
    rating = serializers.DecimalField(
        max_digits=2, decimal_places=1, read_only=True)
    price_range = serializers.ListField(child=serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True), allow_empty=True)
    quantity = serializers.IntegerField(read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        exclude = ('rating_accumulate', 'rating_count')
        read_only_fields = ('created_at', 'updated_at')

    def get_is_favorite(self, obj):
        return obj.customuser_set.filter(id=self.context['request'].user.id).exists()


class ProductFavoriteSerializer(serializers.Serializer):
    is_favorite = serializers.BooleanField()
