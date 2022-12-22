from rest_framework import generics
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model

from users.serializers import UserInfoSerializer, UserUpdateSerializer


@extend_schema(methods=['PUT'], exclude=True)
class UserInfoDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserInfoSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserUpdateSerializer
        return super().get_serializer_class()

    def put(self):
        pass

    def get_object(self):
        return self.request.user
