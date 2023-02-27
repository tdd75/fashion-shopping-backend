from rest_framework import viewsets, mixins, generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
import requests

from products.models import Product
from products.views import ProductViewSet
from products.serializers import ProductSerializer
from .serializers import ChatSerializer, ChatConversationListSerializer, ChatbotMessageSerializer
from .models import ChatMessage


class ChatViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ChatMessage.objects.all().select_related('receiver', 'sender')
    serializer_class = ChatSerializer
    filter_backends = (
        filters.OrderingFilter,
    )
    ordering = ('created_at',)

    def get_queryset(self):
        return ChatMessage.objects.has_owned(self.request.user.id)

    @action(detail=False, methods=['get'], url_path='admin-info')
    def get_admin_info(self, request, *args, **kwargs):
        admin = get_user_model().objects.filter(username='admin').first()
        return Response({
            'id': admin.id,
            'full_name': admin.full_name,
            'avatar': admin.avatar.url if admin.avatar else None,
        }, status=status.HTTP_200_OK)


class ChatConversationListAdminAPIView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ChatConversationListSerializer
    queryset = ChatMessage.objects.all()

    def get_queryset(self):
        return ChatMessage.objects.last_messages(self.request.user.id)


class ChatMessageAdminAPIView(generics.ListAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatSerializer
    filter_backends = (
        filters.OrderingFilter,
    )
    ordering = ('created_at',)

    def get_queryset(self):
        return ChatMessage.objects.has_owned(self.kwargs.get('pk'))


class ChatbotViewSet(generics.GenericAPIView):
    serializer_class = ChatbotMessageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data['message']
        init_chatbot_at = serializer.validated_data['init_chatbot_at']

        response = ChatMessage.objects.call_rasa(message)
        # Rasa error
        if not response:
            return Response([{
                'recipient_id': 'default',
                'text': 'Sorry, something went wrong. Please try again.'
            }], status=status.HTTP_200_OK)

        fallback_msg = response.pop() if len(response) > 1 else None
        processed_msgs = [(ChatMessage.objects.process_msg(
            request, msg, init_chatbot_at) or fallback_msg) for msg in response]

        return Response(processed_msgs, status=status.HTTP_200_OK)
