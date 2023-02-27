from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ChatViewSet, ChatConversationListAdminAPIView, ChatMessageAdminAPIView, ChatbotViewSet

router = DefaultRouter()
router.register('', ChatViewSet)


urlpatterns = [
    *router.urls,
    path('chatbot/', ChatbotViewSet.as_view(), name='chatbot'),
    path('admin/conversations/',
         ChatConversationListAdminAPIView.as_view(), name='admin-conversations'),
    path('admin/conversations/<int:pk>/',
         ChatMessageAdminAPIView.as_view(), name='admin-messages'),
]
