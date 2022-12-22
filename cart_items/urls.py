from django.urls import path

from .views import CartItemListCreateAPIView, CartItemDetailUpdateDeleteAPIView

urlpatterns = [
    path('', CartItemListCreateAPIView.as_view(), name='cart_item_list_create'),
    path('<int:pk>/', CartItemDetailUpdateDeleteAPIView.as_view(),
         name='cart_item_detail_update_delete'),
]
