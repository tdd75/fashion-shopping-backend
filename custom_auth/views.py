from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import OpenApiExample, extend_schema_view, extend_schema
from django.contrib.auth import get_user_model

from .serializers import LoginSerializer, RegisterSerializer, OauthGoogleTokenObtainPairSerializer, OauthFacebookTokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(examples=[
        OpenApiExample(
            'Customer account',
            value={
                'identify': 'tranducduy7520@gmail.com',
                'password': 'duytd123'
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
                    'identify': 'tranducduy7520@gmail.com',
                    'password': 'duytd123',
                    'first_name': 'Duy',
                    'last_name': 'Tran',
                }
            ),
        ]
    )
)
class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer


class OauthGoogleAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = OauthGoogleTokenObtainPairSerializer


class OauthFacebookAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = OauthFacebookTokenObtainPairSerializer
