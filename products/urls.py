from django.urls import path

from .views import ProductListCreateAPIView, ProductDetailUpdateDeleteAPIView

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('<int:pk>/', ProductDetailUpdateDeleteAPIView.as_view(),
         name='product_detail_update_delete'),

]
