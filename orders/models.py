from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .helpers import generate_code
from cart.models import CartItem
from addresses.models import Address
from discount_tickets.models import DiscountTicket


class Order(models.Model):
    class Stage(models.TextChoices):
        TO_PAY = 'TO_PAY', _('To pay')
        TO_SHIP = 'TO_SHIP', _('To ship')
        TO_RECEIVE = 'TO_RECEIVE', _('To receive')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')

    code = models.CharField(max_length=12,
                            unique=True, default=generate_code)
    stage = models.CharField(
        max_length=32, choices=Stage.choices, default=Stage.TO_PAY)
    order_items = models.ManyToManyField(CartItem, blank=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    discount_ticket = models.ForeignKey(
        DiscountTicket, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL)
    # backup_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def amount(self):
        return sum(cart_item.amount for cart_item in self.cartitem_set.all())

    def __str__(self):
        return self.code
