from rest_framework import viewsets, mixins, generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model

from .serializers import ChatSerializer, ChatConversationListSerializer
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
