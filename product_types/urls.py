from django.urls import path

from .views import ProductTypeListCreateAPIView, ProductTypeDetailUpdateDeleteAPIView

urlpatterns = [
    path('', ProductTypeListCreateAPIView.as_view(), name='product_list_create'),
    path('<int:pk>/', ProductTypeDetailUpdateDeleteAPIView.as_view(),
         name='product_detail_update_delete'),
]
