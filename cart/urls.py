from rest_framework.routers import DefaultRouter

from .views import CartItemListCreateUpdateDestroyViewSet

router = DefaultRouter()
router.register('', CartItemListCreateUpdateDestroyViewSet,
                basename='cart_item')

urlpatterns = [
    *router.urls
]
