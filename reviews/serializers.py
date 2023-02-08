from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Review
from custom_users.serializers import UserShortSerializer


class ReviewSerializer(FlexFieldsModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    expandable_fields = {
        'owner': UserShortSerializer,
    }

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('product',)