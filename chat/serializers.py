from rest_flex_fields import FlexFieldsModelSerializer

from .models import ChatMessage


class ChatMessageSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = ChatMessage
        fields = '__all__'
