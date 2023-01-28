from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from rest_flex_fields import FlexFieldsModelSerializer

from .validators import only_int
from .models import ForgotPasswordCode


class LoginSerializer(TokenObtainPairSerializer):
    identify = serializers.CharField(allow_null=False)
    username_field = 'identify'


class OauthTokenObtainPairSerializer(serializers.Serializer):
    token = serializers.CharField()


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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(validators=[validate_password])
    new_password = serializers.CharField(validators=[validate_password])

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise ValidationError({'old_password': 'Wrong password'})


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        is_exists = get_user_model().objects.filter(email=value).exists()
        if not is_exists:
            raise ValidationError({'email': 'This email is not registered'})
        return value


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(validators=[only_int])

    def validate(self, attrs):
        valid_record = ForgotPasswordCode.objects.get_valid_record(
            attrs['email'], attrs['code'])
        if not valid_record:
            raise ValidationError({'code': 'Code invalid'})
        return super().validate(attrs)


class RecoverPasswordSerializer(VerifyCodeSerializer):
    new_password = serializers.CharField(validators=[validate_password])
