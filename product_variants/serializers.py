from rest_flex_fields import FlexFieldsModelSerializer

from .models import ProductVariant


class ProductVariantSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

    expandable_fields = {
        'product': 'products.serializers.ProductSerializer'
    }

class ProductAdminVariantSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

