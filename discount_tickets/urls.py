from rest_framework.routers import DefaultRouter

from .views import DiscountTicketViewSet

router = DefaultRouter()
router.register('', DiscountTicketViewSet, basename='discount_ticket')

urlpatterns = [
    *router.urls
]
