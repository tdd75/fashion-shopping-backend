from rest_framework import serializers

from .models import Review
from users.serializers import UserShortInfoSerializer


class ReviewSerializer(serializers.ModelSerializer):
    owner = UserShortInfoSerializer(read_only=True)

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
