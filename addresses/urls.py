from django.urls import path

from .views import AddressListCreateAPIView, AddressDetailUpdateDeleteAPIView

urlpatterns = [
    path('', AddressListCreateAPIView.as_view(), name='address_list_create'),
    path('addresses/', AddressDetailUpdateDeleteAPIView.as_view(),
         name='address_detail_update_delete'),
]
