from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Address


class AddressSerializer(FlexFieldsModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = '__all__'
