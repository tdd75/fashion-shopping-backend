from django.urls import path

from .views import UserInfoDetailUpdateAPIView

urlpatterns = [
    path('me/', UserInfoDetailUpdateAPIView.as_view(), name='user_info'),
]
