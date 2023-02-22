from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Order
from .serializers import OrderSerializer, OrderAdminSerializer


class OrderListCreateDetailViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                                   mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = ('stage',)
    search_fields = ('code',)
    ordering = ('-updated_at',)

    def get_queryset(self):
        return Order.objects.has_owned(self.request.user.id) \
            .select_related('address', 'discount_ticket').prefetch_related('cartitem_set')

    def perform_create(self, serializer):
        if serializer.validated_data['payment_method'] == Order.PaymentMethod.COD:
            return serializer.save(stage=Order.Stage.TO_SHIP)
        return serializer.save()

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        instance = self.get_object()
        if instance.stage == Order.Stage.TO_PAY:
            instance.stage = Order.Stage.CANCELLED
            instance.save()
            return Response({'message': 'Cancelled succssfully.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Orders cannot be canceled.'}, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['post'], url_path='get-amount')
    # def get_amount(self, request, pk=None):
    #     ticket = self.get_object()
    #     ticket.saved_users.add(request.user.id)
    #     return Response({'message': 'Save succssfully.'}, status=status.HTTP_200_OK)


class OrderAdminViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderAdminSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = ('stage',)
    search_fields = ('code',)
    ordering = ('-updated_at',)
