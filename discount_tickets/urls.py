from django.urls import path

from .views import DiscountTicketListCreateAPIView, DiscountTicketDetailUpdateDeleteAPIView

urlpatterns = [
    path('', DiscountTicketListCreateAPIView.as_view(),
         name='discount_ticket_list_create'),
    path('<int:pk>/', DiscountTicketDetailUpdateDeleteAPIView.as_view(),
         name='discount_ticket_detail_update_delete'),

]
