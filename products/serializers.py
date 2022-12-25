from rest_framework import serializers

from .models import Product
from product_types.serializers import ProductTypeDetailSerializer


class ProductSerializer(serializers.ModelSerializer):
    types = ProductTypeDetailSerializer(
        source='producttype_set', many=True, required=False)
    rating = serializers.ReadOnlyField()

    class Meta:
        model = Product
        exclude = ('rating_accumulate', 'rating_count')
        read_only_fields = ('created_at', 'updated_at', 'rating')
