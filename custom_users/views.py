from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from custom_users.serializers import UserSerializer


class UserInfoDetailUpdateViewSet(mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
