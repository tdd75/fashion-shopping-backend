from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Review
from users.serializers import UserInfoSerializer


class UserShortInfoSerializer(UserInfoSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'full_name',)


class ReviewSerializer(serializers.ModelSerializer):
    user = UserShortInfoSerializer()

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
