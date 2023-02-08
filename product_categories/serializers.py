from rest_flex_fields import FlexFieldsModelSerializer

from .models import ProductCategory


class ProductCategorySerializer(FlexFieldsModelSerializer):
    expandable_fields = {
        'products': ('products.serializers.ProductSerializer', {'many': True, 'source': 'product_set'})
    }

    class Meta:
        model = ProductCategory
        fields = '__all__'
