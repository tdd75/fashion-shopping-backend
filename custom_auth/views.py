from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import OpenApiExample, extend_schema_view, extend_schema
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone

from .serializers import LoginSerializer, RegisterSerializer, OauthGoogleTokenObtainPairSerializer, OauthFacebookTokenObtainPairSerializer,\
    ChangePasswordSerializer, ForgotPasswordSerializer, VerifyCodeSerializer, RecoverPasswordSerializer
from .models import ForgotPasswordCode


@extend_schema_view(
    post=extend_schema(examples=[
        OpenApiExample(
            'Admin account',
            value={
                'identify': 'admin',
                'password': 'admin',
            },
        ),
        OpenApiExample(
            'Customer account',
            value={
                'identify': 'tranducduy7520@gmail.com',
                'password': 'duytd123',
            },
        ),
    ])
)
class MyObtainTokenPairAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


@extend_schema_view(
    post=extend_schema(
        auth=[],
        examples=[
            OpenApiExample(
                'Customer account',
                value={
                    'email': 'tranducduy7520@gmail.com',
                    'username': 'tranducduy7520',
                    'phone': '0834275110',
                    'password': 'duytd123',
                    'first_name': 'Duy',
                    'last_name': 'Tran',
                }
            ),
        ]
    )
)
class OauthGoogleAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = OauthGoogleTokenObtainPairSerializer


class OauthFacebookAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = OauthFacebookTokenObtainPairSerializer


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        user = self.request.user
        # check old password
        if not user.check_password(validated_data['old_password']):
            raise ParseError({'old_password': 'Wrong password'})
        # set new password
        user.set_password(validated_data['new_password'])
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ForgotPasswordView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def perform_create(self, serializer):
        serializer.save(expired_at=timezone.now() +
                        timezone.timedelta(minutes=5))

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        UserModel = get_user_model()
        # check email
        user = UserModel.objects.filter(email=validated_data['email']).first()
        if not user:
            raise ParseError({'email': 'This email is not registered'})
        # generate code
        code = get_random_string(length=6, allowed_chars='0123456789')
        # send email
        send_mail(f'Forgot password', f'{code}', None,
                  [validated_data['email']], fail_silently=False)
        # save code to database
        ForgotPasswordCode.objects.create(
            user=user, code=code)

        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyCodeView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        instance = ForgotPasswordCode.objects.filter(
            user__email=validated_data['email'], code=validated_data['code'],
            expired_at__lte=timezone.now().isoformat(), recover_token__isnull=True).first()
        if not instance:
            raise ParseError({'code': 'Code invalid'})
        instance.recover_token = get_random_string(
            length=12, allowed_chars=['abcdefghjklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'])
        instance.expired_at = timezone.now() + timezone.datetime(minute=5)
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RecoverPasswordView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RecoverPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        instance = ForgotPasswordCode.objects.filter(
            user__email=validated_data['email'], recover_token=validated_data['recover_token'],
            expired_at__lte=timezone.now().isoformat()).first()
        if not instance:
            raise ParseError({'code': 'Token invalid'})
        # set new password
        UserModel = get_user_model()
        user = UserModel.objects.filter(email=validated_data['email']).first()
        user.set_password(validated_data['new_password'])
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
