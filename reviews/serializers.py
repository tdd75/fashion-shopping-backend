from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from custom_users.serializers import UserShortSerializer
from product_variants.serializers import ProductVariantSerializer
from .models import Review


class ReviewSerializer(FlexFieldsModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    expandable_fields = {
        'owner': UserShortSerializer,
        'variant': ProductVariantSerializer
    }

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('product',)
