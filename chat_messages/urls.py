from django.urls import path

from .views import ChatMessageListCreateAPIView, ChatMessageDetailUpdateDeleteAPIView

urlpatterns = [
    path('', ChatMessageListCreateAPIView.as_view(),
         name='discount_ticket_list_create'),
    path('<int:pk>/', ChatMessageDetailUpdateDeleteAPIView.as_view(),
         name='discount_ticket_detail_update_delete'),
]
