from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer

from .models import Product


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Macbook Pro M1 14',
            value={
                'name': 'Macbook Pro M1',
                'image': 'https://www.maccenter.vn/App_images/MacBookPro-14-Silver-A.jpg',
                'description': 'MacBook Pro 14-inch chip M1 Pro 16GB + 512GB (Silver)',
                'price': '2000',
                'rating': '5',
                'available': 4,
            },
        ),
    ]
)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description',
                  'price', 'rating', 'available']
