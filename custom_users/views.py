from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from custom_users.serializers import UserSerializer


@extend_schema(methods=['PUT'], exclude=True)
class UserInfoDetailUpdateViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def put(self):
        pass
