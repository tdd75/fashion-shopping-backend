from django.db import models
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException

from orders.models import Order
from .payment_gateway.paypal import paypal_payment


class TransactionQuerySet(models.QuerySet):
    def has_owned(self, user_id):
        return self.filter(owner_id=user_id)


class TransactionManager(models.Manager):
    def _create_paypal_order(self, order_items):
        data = [{
            'reference_id': item.product_variant.id,
            'description': f'{item.product_variant.product.name} | {item.product_variant.color} | {item.product_variant.size}',
            'soft_descriptor': item.product_variant.product.name,
            'amount': {
                'currency_code': 'USD',
                'value': str(item.product_variant.price),
            },
        } for item in order_items]
        return paypal_payment.request_order(data)

    def create_order(self, order):
        order_items = order.cartitem_set.all()
        payment_method = order.payment_method

        order_data = None
        if payment_method == Order.PaymentMethod.PAYPAL:
            order_data = self._create_paypal_order(order_items)

        if not order_data:
            assert APIException('Something went wrong when create order.')

        return self.create(order=order,
                           payment_link=order_data['payment_link'],
                           check_payment_link=order_data['check_payment_link'])

    def remove_old_transaction(self, order_id):
        return self.filter(order_id=order_id, paid_at__isnull=True).delete()
