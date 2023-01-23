from rest_framework.routers import DefaultRouter

from .views import ProductTypeViewSet

router = DefaultRouter()
router.register('', ProductTypeViewSet, basename='product_type')

urlpatterns = [
    *router.urls
]
