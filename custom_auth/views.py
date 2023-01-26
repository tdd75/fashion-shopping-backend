from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.contrib.auth import get_user_model

from .serializers import *
from .swagger import *
from . import services


@extend_schema_view(post=extend_schema(examples=LOGIN_EXAMPLES))
class MyObtainTokenPairAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class OauthGoogleAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = OauthTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = services.oauth_google(**serializer.data)
        return Response(res, status=status.HTTP_200_OK)


class OauthFacebookAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = OauthTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = services.oauth_google(**serializer.data)
        return Response(res, status=status.HTTP_200_OK)


@extend_schema_view(post=extend_schema(auth=[], examples=REGISTER_EXAMPLES))
class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        services.register(**serializer.data,
                          password=self.request.data['password'])


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.change_password(**serializer.data, user=self.request.user)
        return Response({'message': 'Change password successfully.'}, status=status.HTTP_200_OK)


@extend_schema_view(post=extend_schema(auth=[], examples=FORGOT_PASSWORD_EXAMPLES))
class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.send_forgot_password_code(**serializer.data)
        return Response({'message': 'Send email successfully.'}, status=status.HTTP_200_OK)


@extend_schema_view(post=extend_schema(auth=[]))
class VerifyCodeView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.verify_code(**serializer.data)
        return Response({'message': 'Code was verified.'}, status=status.HTTP_200_OK)


@extend_schema_view(post=extend_schema(auth=[]))
class RecoverPasswordView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RecoverPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.verify_code(**serializer.data)
        services.recover_password(**serializer.data)
        return Response({'message': 'Recoverd password.'}, status=status.HTTP_200_OK)
