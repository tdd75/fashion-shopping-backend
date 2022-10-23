from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from google.oauth2 import id_token
from google.auth.transport import requests

from users.models import CustomUser
from django.conf import settings


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class OauthGoogleTokenObtainPairSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id_token = serializers.CharField(required=True)

    class Meta:
        fields = ['id_token']

    def validate(self, data):
        id_info = id_token.verify_oauth2_token(
            data['id_token'], requests.Request(), settings.OAUTH_GOOGLE_CLIENT_ID)

        user_existed = CustomUser.objects.filter(
            email__exact=id_info['email']).first()

        if not user_existed:
            user = CustomUser.objects.create(
                username=id_info['email'],
                email=id_info['email'],
                first_name=id_info['given_name'],
                last_name=id_info['family_name']
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
