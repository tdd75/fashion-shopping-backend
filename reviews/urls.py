from django.urls import path

from .views import ReviewListCreateAPIView, ReviewDetailUpdateDeleteAPIView

urlpatterns = [
    path('', ReviewListCreateAPIView.as_view(), name='review_list_create'),
    path('<int:pk>/', ReviewDetailUpdateDeleteAPIView.as_view(),
         name='review_detail_update_delete'),
]
