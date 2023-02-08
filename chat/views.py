from rest_framework import viewsets, mixins, filters

from .serializers import ChatMessageSerializer
from .models import ChatMessage


class ChatMessageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ChatMessage.objects.all().select_related('receiver', 'sender')
    serializer_class = ChatMessageSerializer
    filter_backends = (
        filters.OrderingFilter,
    )
    ordering = ('-created_at',)

    def get_queryset(self):
        return ChatMessage.objects.has_owned(self.request.user.id)

    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = serializer.validated_data

    #     msg = ChatMessage.objects.create(**data)
    #     # socket_message = f'Message with id {msg.id} was created!'
    #     # channel_layer = get_channel_layer()
    #     # async_to_sync(channel_layer.group_send)(
    #     #     f'{request.user.id}-message', {
    #     #         'type': 'send_last_message',
    #     #         'text': socket_message
    #     #     }
    #     # )

    #     return Response({'status': True}, status=status.HTTP_201_CREATED)

