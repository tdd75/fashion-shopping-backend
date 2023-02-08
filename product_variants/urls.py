from rest_framework.routers import DefaultRouter

from .views import ProductVariantViewSet

router = DefaultRouter()
router.register('', ProductVariantViewSet)

urlpatterns = [
    *router.urls
]
