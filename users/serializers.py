from rest_framework import serializers
from django.contrib.auth import get_user_model

from addresses.serializers import AddressSerializer


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        exclude = ('password',)
        depth = 1

class UserShortInfoSerializer(UserDetailSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'full_name')
