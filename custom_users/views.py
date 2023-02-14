from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser

from custom_users.serializers import UserSerializer, UserAdminSerializer


class UserInfoDetailUpdateViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdminUser,)
