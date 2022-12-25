from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Address


class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    address = AddressUpdateSerializer()
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        exclude = ('password',)


class UserShortInfoSerializer(UserDetailSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'full_name')


class UserUpdateSerializer(serializers.ModelSerializer):
    address = AddressUpdateSerializer()

    class Meta:
        model = get_user_model()
        fields = ('username', 'phone', 'first_name',
                  'last_name', 'avatar', 'address')

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')

        if not instance.address:
            instance.address_id = Address.objects.create(**address_data)
        else:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()

        return super().update(instance, validated_data)
