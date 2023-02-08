from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from asgiref.sync import sync_to_async, async_to_sync

from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope['user'] is not AnonymousUser:
            self.user_id = self.scope['user'].id
            self.room_group_name = f'{self.user_id}-message'
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def _create_message(self, data):
        data['sender_id'] = self.user_id
        data['receiver_id'] = data.pop('receiver', None)
        instance = ChatMessage.objects.create(**data)
        return ChatMessageSerializer(instance, expand=('receiver', 'sender')).data

    async def receive_json(self, content):
        response = await sync_to_async(self._create_message)(content)
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': response,
        })

    async def chat_message(self, event):
        await self.send_json(event['message'])
