from django.urls import path

from .views import TransactionListCreateAPIView, TransactionDetailUpdateDeleteAPIView

urlpatterns = [
    path('', TransactionListCreateAPIView.as_view(), name='transaction_list_create'),
    path('<int:pk>/', TransactionDetailUpdateDeleteAPIView.as_view(),
         name='transaction_detail_update_delete'),
]
