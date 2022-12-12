from django.urls import path

from .views import UserInfoDetailAPIView

urlpatterns = [
    path('info/', UserInfoDetailAPIView.as_view(), name='user_info'),
]
