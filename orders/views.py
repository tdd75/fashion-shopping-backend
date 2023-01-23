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
        return Order.objects.filter(owner_id=self.request.user.id)
