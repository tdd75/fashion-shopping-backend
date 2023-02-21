from rest_framework.routers import DefaultRouter

from .views import ProductVariantViewSet, ProductAdminVariantViewSet

router = DefaultRouter()
router.register('admin', ProductAdminVariantViewSet)
router.register('', ProductVariantViewSet)

urlpatterns = [
    *router.urls
]
