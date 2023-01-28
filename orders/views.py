from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Order
from .serializers import OrderSerializer


class OrderListCreateDetailViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                                   mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_fields = ('stage',)
    search_fields = ('code',)

    def get_queryset(self):
        return Order.objects.has_owned(self.request.user.id) \
            .select_related('address', 'discount_ticket').prefetch_related('order_items')

    def create(self, request, *args, **kwargs):
        instance = super().create(request, *args, **kwargs)
        return instance
