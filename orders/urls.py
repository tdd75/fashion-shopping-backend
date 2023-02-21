from rest_framework.routers import DefaultRouter

from .views import OrderListCreateDetailViewSet, OrderAdminViewSet

router = DefaultRouter()
router.register('admin', OrderAdminViewSet)
router.register('', OrderListCreateDetailViewSet)

urlpatterns = [
    *router.urls
]
