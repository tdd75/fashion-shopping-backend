from rest_framework import generics
from users.models import CustomUser

from users.serializers import UserInfoSerializer


class UserInfoDetailAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user
