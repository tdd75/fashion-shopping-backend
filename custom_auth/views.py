from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema_view, extend_schema

from api.views import PostAPIView
from .serializers import *
from .swagger import *


@extend_schema_view(post=extend_schema(examples=LOGIN_EXAMPLES))
class LoginAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


@extend_schema_view(post=extend_schema(examples=ADMIN_LOGIN_EXAMPLES))
class AdminLoginAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = AdminLoginSerializer


class OauthGoogleAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OauthTokenObtainPairSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = ForgotPasswordCode.objects.oauth_google(
            serializer.validated_data['token'])

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class OauthFacebookAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OauthTokenObtainPairSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = ForgotPasswordCode.objects.oauth_facebook(
            serializer.validated_data['token'])

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


@extend_schema_view(post=extend_schema(auth=[], examples=REGISTER_EXAMPLES))
class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        get_user_model().objects.create_user(data['email'], data['password'])

        return Response({'message': 'Register successfully'}, status=status.HTTP_201_CREATED)


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.change_password(
            serializer.validated_data['new_password'])

        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


@extend_schema_view(post=extend_schema(auth=[], examples=FORGOT_PASSWORD_EXAMPLES))
class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ForgotPasswordCode.objects.send_otp(serializer.validated_data['email'])

        return Response({
            'message': 'Code sent to email'
        }, status=status.HTTP_200_OK)


@extend_schema_view(post=extend_schema(auth=[]))
class VerifyCodeView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            'message': 'Code verified'
        }, status=status.HTTP_200_OK)


@extend_schema_view(post=extend_schema(auth=[]))
class RecoverPasswordView(PostAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RecoverPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = get_user_model().objects.get_by_email(data['email'])
        user.change_password(data['new_password'])

        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)
