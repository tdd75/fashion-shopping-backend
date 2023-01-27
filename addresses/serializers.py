from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Address


class AddressSerializer(FlexFieldsModelSerializer):
    is_default = serializers.BooleanField(read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = '__all__'
