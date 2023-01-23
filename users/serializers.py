from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        exclude = ('password',)


class UserShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'full_name')
