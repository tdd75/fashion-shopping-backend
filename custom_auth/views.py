from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema_view, extend_schema

from .serializers import *
from .swagger import *
from api.views import PostAPIView


@extend_schema_view(post=extend_schema(examples=LOGIN_EXAMPLES))
class MyObtainTokenPairAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class OauthGoogleAPIView(PostAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OauthGoogleObtainPairSerializer


class OauthFacebookAPIView(PostAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OauthFacebookObtainPairSerializer


@extend_schema_view(post=extend_schema(auth=[], examples=REGISTER_EXAMPLES))
class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer


class ChangePasswordView(PostAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer


@extend_schema_view(post=extend_schema(auth=[], examples=FORGOT_PASSWORD_EXAMPLES))
class ForgotPasswordView(PostAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer


@extend_schema_view(post=extend_schema(auth=[]))
class VerifyCodeView(PostAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyCodeSerializer


@extend_schema_view(post=extend_schema(auth=[]))
class RecoverPasswordView(PostAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RecoverPasswordSerializer
