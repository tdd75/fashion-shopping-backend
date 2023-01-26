from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(FlexFieldsModelSerializer):
    full_name = serializers.CharField(read_only=True)
    avatar = Base64ImageField()

    class Meta:
        model = get_user_model()
        exclude = ('password',)


class UserShortSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'full_name')
