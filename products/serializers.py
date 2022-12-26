from rest_framework import serializers

from .models import Product
from product_types.serializers import ProductTypeDetailSerializer


class ProductSerializer(serializers.ModelSerializer):
    types = ProductTypeDetailSerializer(
        source='producttype_set', many=True, required=False)
    rating = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        exclude = ('rating_accumulate', 'rating_count')
        read_only_fields = ('created_at', 'updated_at')
