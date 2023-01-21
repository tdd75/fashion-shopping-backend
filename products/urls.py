from django.urls import path

from .views import ProductListCreateAPIView, ProductDetailAPIView, ProductFavoriteAPIView

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('<int:pk>/', ProductDetailAPIView.as_view(),
         name='product_detail'),
    path('<int:pk>/favorite', ProductFavoriteAPIView.as_view(),
         name='add_favorite_product'),
]
