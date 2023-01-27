from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Address


class AddressSerializer(FlexFieldsModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = '__all__'

    def save(self, **kwargs):
        is_default = self.validated_data.get('is_default')
        if is_default == True:
            Address.objects.filter(owner=self.context['request'].user,
                                   is_default=True).update(is_default=False)
        return super().save(**kwargs)
