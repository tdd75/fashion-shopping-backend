from rest_framework.routers import DefaultRouter

from .views import AddressViewSet

router = DefaultRouter()
router.register('', AddressViewSet)

urlpatterns = [
    *router.urls
]
