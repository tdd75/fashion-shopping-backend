from django.urls import path

from .views import OrderListCreateAPIView, OrderDetailUpdateAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order_list_create'),
    path('<int:pk>/', OrderDetailUpdateAPIView.as_view(),
         name='order_detail_update'),
]
