from rest_framework import viewsets

from .serializers import ChatMessageSerializer
from .models import ChatMessage


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
