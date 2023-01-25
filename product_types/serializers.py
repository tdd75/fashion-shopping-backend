from rest_flex_fields import FlexFieldsModelSerializer

from .models import ProductType


class ProductTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

    expandable_fields = {
        'product': 'products.serializers.ProductSerializer'
    }
