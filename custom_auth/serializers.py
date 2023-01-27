from django.db.models import Q
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_flex_fields import FlexFieldsModelSerializer
import requests

from .validators import only_int
from .models import ForgotPasswordCode


class LoginSerializer(TokenObtainPairSerializer):
    identify = serializers.CharField(allow_null=False)
    username_field = 'identify'


class _OauthTokenObtainPairSerializer(serializers.Serializer):
    token = serializers.CharField()

    def trigger_login(self, user_info: dict):
        user = get_user_model().objects.filter(
            email=user_info['email']).first()
        if not user:
            user = get_user_model().objects.create(
                username=user_info['email'],
                **user_info,
            )
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
        return RefreshToken.for_user(user)


class OauthGoogleObtainPairSerializer(_OauthTokenObtainPairSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        oauth_url = f'https://oauth2.googleapis.com/tokeninfo?id_token={data["token"]}'
        response = requests.get(oauth_url).json()
        if response.get('error'):
            raise AuthenticationFailed('Invalid token')
        user_info = {
            'email': response['email'],
            'first_name': response['given_name'],
            'last_name': response['family_name'],
        }
        refresh = super().trigger_login(user_info)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class OauthFacebookObtainPairSerializer(_OauthTokenObtainPairSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        oauth_url = f'https://graph.facebook.com/me?fields=first_name,last_name,email,picture&access_token={data["token"]}'
        response = requests.get(oauth_url).json()
        if response.get('error'):
            raise AuthenticationFailed('Invalid token')
        user_info = {
            'email': response['email'],
            'first_name': response['first_name'],
            'last_name': response['last_name'],
        }
        refresh = super().trigger_login(user_info)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class RegisterSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(validators=[validate_password])

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def validate_email(self, value):
        user = get_user_model().objects.filter(Q(email=value)).first()
        if user and user.password:
            raise ValidationError(f'Email is already in use')
        return value

    def validate_username(self, value):
        user = get_user_model().objects.filter(Q(username=value)).first()
        if user and user.password:
            raise ValidationError(f'Username is already in use')
        return value

    def save(self, **kwargs):
        data = self.validated_data
        user = get_user_model().objects.create(
            email=data['email'], username=data['username'])
        user.set_password(data['password'])
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(validators=[validate_password])
    new_password = serializers.CharField(validators=[validate_password])

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise ValidationError({'old_password': 'Wrong password'})

    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        user.set_password(data['new_password'])
        user.save()
        return {
            'message': 'Password changed successfully'
        }


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        is_exists = get_user_model().objects.filter(email=value).exists()
        if not is_exists:
            raise ValidationError({'email': 'This email is not registered'})
        return value

    def save(self, **kwargs):
        data = self.validated_data
        code = get_random_string(length=6, allowed_chars='0123456789')
        send_mail(f'Forgot password', f'{code}', None,
                  [data['email']], fail_silently=False)
        ForgotPasswordCode.objects.create(user=get_user_model().objects.get(email=data['email']),
                                          code=code,
                                          expired_at=timezone.now() +
                                          timezone.timedelta(minutes=settings.OTP_EXPIRE_MINUTES))
        return {
            'message': 'Code sent to email'
        }


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(validators=[only_int])

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        instance = ForgotPasswordCode.objects.filter(
            user__email=attrs['email'], code=attrs['code'],
            expired_at__gte=timezone.now().isoformat()).exists()
        if not instance:
            raise ValidationError({'code': 'Code invalid'})
        return super().validate(attrs)


class RecoverPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])

    def validate(self, attrs):
        VerifyCodeSerializer.validate(self, attrs)
        return super().validate(attrs)

    def save(self, **kwargs):
        data = self.validated_data
        user = get_user_model().objects.filter(
            email=data['email']).first()
        user.set_password(data['new_password'])
        user.save()
        return {
            'message': 'Password changed successfully'
        }
