from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import OpenApiExample, extend_schema_view, extend_schema

from .serializers import RegisterSerializer, OauthGoogleTokenObtainPairSerializer
from users.models import CustomUser


@extend_schema_view(
    post=extend_schema(examples=[
        OpenApiExample(
            'Customer account',
            value={
                'email': 'duy.td183515@sis.hust.edu.vn',
                'password': 'DATN_KS_20221'
            },
        ),
    ])
)
class MyObtainTokenPairAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(examples=[
        OpenApiExample(
            'Customer account',
            value={
                'email': 'duy.td183515@sis.hust.edu.vn',
                'password': 'DATN_KS_20221',
                'first_name': 'Duy',
                'last_name': 'Tran',
            }
        ),
    ])
)
class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class OauthGoogleAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = OauthGoogleTokenObtainPairSerializer
