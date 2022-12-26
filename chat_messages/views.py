from rest_framework import generics

from .serializers import ChatMessageSerializer
from .models import ChatMessage


class ChatMessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer


class ChatMessageDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    lookup_field = 'pk'
