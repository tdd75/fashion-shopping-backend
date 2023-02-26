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
    def _create_paypal_order(self, order_code, order_items):
        data = [{
            'reference_id': order_code,
            'description': f'{item.product_variant.product.name} | {item.product_variant.color} | {item.product_variant.size}',
            'soft_description': item.product_variant.product.name,
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
            order_data = self._create_paypal_order(order.code, order_items)

        if not order_data:
            raise APIException('Something went wrong when create order.')

        return self.create(order=order,
                           payment_link=order_data['payment_link'],
                           check_payment_link=order_data['check_payment_link'])

    def remove_old_transaction(self, order_id):
        if self.filter(order_id=order_id, paid_at__isnull=False):
            return False
        else:
            self.filter(order_id=order_id, paid_at__isnull=True).delete()
            return True
        
    def check_order_paypal(self, order_id):
        order_data = paypal_payment.check_order_completed(order_id)
        if order_data:
            instance = self.filter(order__code=order_data['code']).first()
            if instance:
                instance.paid_amount = order_data['paid_amount']
                instance.paid_at = order_data['paid_at']
                instance.order.stage = Order.Stage.TO_SHIP
                instance.save()
                instance.order.save()
                return True
        
        return False