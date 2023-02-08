from rest_framework.routers import DefaultRouter

from .views import ProductCategoryViewSet

router = DefaultRouter()
router.register('', ProductCategoryViewSet)

urlpatterns = [
    *router.urls
]
