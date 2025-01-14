from rest_framework.routers import DefaultRouter

from .views import ReviewListCreateViewSet

router = DefaultRouter()
router.register('', ReviewListCreateViewSet)

urlpatterns = [
    *router.urls
]
