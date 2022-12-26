import requests
from abc import abstractmethod
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError, ParseError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model


class LoginSerializer(TokenObtainPairSerializer):
    identify = serializers.CharField(allow_null=False)
    username_field = 'identify'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        validators=[validate_password], write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'phone',
                  'first_name', 'last_name', 'password',)
        optional_fields = ('username', 'phone')

    def create(self, validated_data):
        UserModel = get_user_model()

        user_existed = UserModel.objects.filter(
            email=validated_data['email']).first()
        if user_existed:
            if user_existed.password:
                raise ValidationError('This email is already in use')
        else:
            password = validated_data.pop('password')
            user = UserModel.objects.create(**validated_data)
            user.set_password(password)
            user.save()

        return user


class OauthTokenObtainPairSerializer(serializers.Serializer):
    token = serializers.CharField()

    class Meta:
        fields = ['token']

    @abstractmethod
    def get_user_info(self, token):
        pass

    def validate(self, data):
        UserModel = get_user_model()
        user_info = self.get_user_info(data['token'])

        user_existed = UserModel.objects.filter(
            email=user_info['email']).first()

        if not user_existed:
            user = UserModel.objects.create(
                username=user_info['email'],
                **user_info,
            )
        else:
            user = user_existed

        response = {}
        refresh = RefreshToken.for_user(user)

        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return response


class OauthGoogleTokenObtainPairSerializer(OauthTokenObtainPairSerializer):
    def get_user_info(self, token):
        response = requests.get(
            f'https://oauth2.googleapis.com/tokeninfo?id_token={token}').json()
        if response.get('error'):
            raise AuthenticationFailed('Invalid token')

        user_info = {
            'email': response['email'],
            'first_name': response['given_name'],
            'last_name': response['family_name'],
        }
        return user_info


class OauthFacebookTokenObtainPairSerializer(OauthTokenObtainPairSerializer):
    def get_user_info(self, token):
        response = requests.get(
            f'https://graph.facebook.com/me?fields=first_name,last_name,email,picture&access_token={token}').json()
        if response.get('error'):
            raise AuthenticationFailed('Invalid token')

        user_info = {
            'email': response['email'],
            'first_name': response['first_name'],
            'last_name': response['last_name'],
        }
        return user_info


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(validators=[validate_password])
    new_password = serializers.CharField(validators=[validate_password])


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


def only_int(value):
    if value.isdigit() == False:
        raise ValidationError('Code can only include numbers')


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(validators=[only_int])


class RecoverPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    recover_token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])