from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelSerializer

from .models import ChatMessage
from custom_users.serializers import UserShortSerializer


class ChatSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

    def get_is_self(self, obj) -> bool | None:
        if not self.context.get('request'):
            return None
        return self.context['request'].user.id == obj.sender.id


class ChatConversationListSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def get_user(self, obj) -> UserShortSerializer:
        user = obj.sender if obj.sender.id != self.context.get(
            'request').user.id else obj.receiver
        return UserShortSerializer(user).data

    def get_last_message(self, obj) -> str:
        return obj.content
