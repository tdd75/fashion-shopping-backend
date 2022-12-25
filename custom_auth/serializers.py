import requests
from abc import ABC, abstractmethod
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model


class LoginSerializer(TokenObtainPairSerializer):
    identify = serializers.CharField(required=True, allow_null=False)
    username_field = 'identify'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True, validators=[validate_password])

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'phone',
                  'password', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
        write_only_fields = ('password',)
        optional_fields = ('username', 'phone')

    def create(self, validated_data):
        UserModel = get_user_model()

        user_existed = UserModel.objects.filter(
            email__exact=validated_data['email']).first()
        if user_existed:
            if user_existed.password:
                raise ValidationError('This email is already in use')
            user = user_existed
        else:
            user = UserModel.objects.create(
                username=validated_data['email'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )

        user.set_password(validated_data['password'])
        user.save()

        return user


class OauthTokenObtainPairSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    class Meta:
        fields = ['token']

    @abstractmethod
    def get_user_info(self, token):
        pass

    def validate(self, data):
        UserModel = get_user_model()
        user_info = self.get_user_info(data['token'])

        user_existed = UserModel.objects.filter(
            email__exact=user_info['email']).first()

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
