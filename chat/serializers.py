from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelSerializer

from .models import ChatMessage
from custom_users.serializers import UserShortSerializer


class ChatMessageSerializer(FlexFieldsModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all())
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all())

    expandable_fields = {
        'receiver': UserShortSerializer,
        'sender': UserShortSerializer,
    }

    class Meta:
        model = ChatMessage
        fields = '__all__'
