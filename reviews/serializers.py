from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Review
from custom_users.serializers import UserShortSerializer


class ReviewSerializer(FlexFieldsModelSerializer):
    owner = UserShortSerializer(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.product.rating_accumulate += validated_data['rating']
        instance.product.rating_count += 1
        instance.product.save()
        return instance
