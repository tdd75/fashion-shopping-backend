from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework.decorators import action

from orders.models import Order
from .serializers import TransactionSerializer
from .models import Transaction


class TransactionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        order_id = serializer.initial_data.get('order')
        # clean up old transaction
        has_access_perm = Order.objects.has_owned(
            request.user.id).filter(pk=order_id).exists()
        if not has_access_perm:
            raise PermissionDenied(
                'You do not have permission to access this order.')
        result = Transaction.objects.remove_old_transaction(order_id)
        if not result:
            raise APIException('This order has been paid.')
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            transaction = Transaction.objects.create_order(data['order'])
        except Exception as e:
            raise APIException(e)
        return Response({'payment_link': transaction.payment_link}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='paypal/webhook', serializer_class=None, permission_classes=())
    def check_paypal(self, request, pk=None):
        result = Transaction.objects.check_order_paypal(request.data['resource']['id'])
        if result:
            return Response({'message': 'Order confirmed.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Order is not confirmed.'}, status=status.HTTP_400_BAD_REQUEST)

class TransactionAdminViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
