from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserInfoDetailUpdateViewSet, UserAdminViewSet

router = DefaultRouter()
router.register('admin', UserAdminViewSet)

urlpatterns = [
]

urlpatterns = [
    path('me/', UserInfoDetailUpdateViewSet.as_view({
        'patch': 'partial_update', 'get': 'retrieve'
    })),
    *router.urls
]
