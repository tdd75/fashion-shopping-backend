from rest_framework import generics
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model

from users.serializers import UserDetailSerializer


@extend_schema(methods=['PUT'], exclude=True)
class UserInfoDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer

    def put(self):
        pass

    def get_object(self):
        return self.request.user
