from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from asgiref.sync import sync_to_async

from .models import ChatMessage
from .serializers import ChatSerializer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if getattr(self.scope['user'], 'id'):
            self.user_id = self.scope['user'].id
            self.room_group_name = '_'.join(
                str(id) for id in sorted([self.user_id, self.scope['receiver']])
            )
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, content):
        """_summary_

        Args:
            content (dict): {
                'content': str
                'receiver': int
            }
        """
        response = await sync_to_async(self._create_message)(content)
        if response:
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': response,
            })

    async def chat_message(self, event):
        await self.send_json(event['message'])

    # private methods
    def _create_message(self, content):
        data = {
            'sender_id': self.user_id,
            'receiver_id': content.pop('receiver', None),
            'content': content.pop('content', None),
        }
        if not data['content'].strip():
            return None
        instance = ChatMessage.objects.create(**data)
        res = ChatSerializer(instance).data
        return res
