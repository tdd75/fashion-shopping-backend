from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Review
from custom_users.serializers import UserShortSerializer


class ReviewSerializer(FlexFieldsModelSerializer):
    owner = UserShortSerializer(
        write_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'
