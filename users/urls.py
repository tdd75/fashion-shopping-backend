from rest_framework.routers import DefaultRouter

from .views import UserInfoDetailUpdateViewSet

router = DefaultRouter()
router.register('me', UserInfoDetailUpdateViewSet, basename='order')

urlpatterns = [
    *router.urls
]
