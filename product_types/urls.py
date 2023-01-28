from rest_framework.routers import DefaultRouter

from .views import ProductTypeViewSet

router = DefaultRouter()
router.register('', ProductTypeViewSet)

urlpatterns = [
    *router.urls
]
