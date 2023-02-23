from rest_framework.routers import DefaultRouter

from .views import DiscountTicketViewSet, DiscountTicketAdminViewSet

router = DefaultRouter()
router.register('admin', DiscountTicketAdminViewSet)
router.register('', DiscountTicketViewSet)

urlpatterns = [
    *router.urls
]
