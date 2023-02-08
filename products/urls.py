from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, ProductAdminViewSet

router = DefaultRouter()
router.register('admin', ProductAdminViewSet)
router.register('', ProductViewSet)

urlpatterns = [
    *router.urls,
]
