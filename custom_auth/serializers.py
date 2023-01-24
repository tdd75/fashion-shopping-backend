import requests
from abc import abstractmethod
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .validators import only_int

from django.contrib.auth import get_user_model


class LoginSerializer(TokenObtainPairSerializer):
    identify = serializers.CharField(allow_null=False)
    username_field = 'identify'


class OauthTokenObtainPairSerializer(serializers.Serializer):
    token = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        validators=[validate_password], write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(validators=[validate_password])
    new_password = serializers.CharField(validators=[validate_password])


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(validators=[only_int])


class RecoverPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
