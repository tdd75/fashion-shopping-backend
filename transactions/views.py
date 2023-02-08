from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


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
        Transaction.objects.remove_old_transaction(order_id)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        transaction = Transaction.objects.create_order(data['order'])
        return Response({'payment_link': transaction.payment_link}, status=status.HTTP_200_OK)


class TransactionAdminViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
