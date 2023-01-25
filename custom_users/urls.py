from django.urls import path

from .views import UserInfoDetailUpdateViewSet


urlpatterns = [
    path('me/', UserInfoDetailUpdateViewSet.as_view({
        'patch': 'partial_update', 'get': 'retrieve'
    }))
]
