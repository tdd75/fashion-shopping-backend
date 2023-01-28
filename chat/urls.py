from rest_framework.routers import DefaultRouter

from .views import ChatMessageViewSet

router = DefaultRouter()
router.register('', ChatMessageViewSet)

urlpatterns = [
    *router.urls
]
