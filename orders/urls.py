from rest_framework.routers import DefaultRouter

from .views import OrderListCreateDetailViewSet

router = DefaultRouter()
router.register('', OrderListCreateDetailViewSet, basename='order')

urlpatterns = [
    *router.urls
]
