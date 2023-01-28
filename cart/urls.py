from rest_framework.routers import DefaultRouter

from .views import CartItemListCreateUpdateDestroyViewSet

router = DefaultRouter()
router.register('', CartItemListCreateUpdateDestroyViewSet)

urlpatterns = [
    *router.urls
]
