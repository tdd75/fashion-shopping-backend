from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj) -> str:
        return obj.first_name + ' ' + obj.last_name

    class Meta:
        model = get_user_model()
        exclude = ('password',)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'phone', 'first_name', 'last_name', 'avatar')
