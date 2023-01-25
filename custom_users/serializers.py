from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    avatar = Base64ImageField()

    class Meta:
        model = get_user_model()
        exclude = ('password',)


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'full_name')
