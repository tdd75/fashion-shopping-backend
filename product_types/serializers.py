from rest_framework import serializers

from .models import ProductType


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class ProductTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        exclude = ('product',)
