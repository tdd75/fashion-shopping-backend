from rest_framework import mixins, viewsets
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model

from custom_users.serializers import UserInfoSerializer


@extend_schema(methods=['PUT'], exclude=True)
class UserInfoDetailUpdateViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user

    def put(self):
        pass
