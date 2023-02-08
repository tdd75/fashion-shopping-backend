from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from api.models import models, BaseModel
from addresses.models import Address
from discount_tickets.models import DiscountTicket
from .helpers import generate_code
from .managers import OrderManager, OrderQuerySet


class Order(BaseModel):
    class Stage(models.TextChoices):
        TO_PAY = 'TO_PAY', _('To pay')
        TO_SHIP = 'TO_SHIP', _('To ship')
        TO_RECEIVE = 'TO_RECEIVE', _('To receive')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')

    class PaymentMethod(models.TextChoices):
        COD = 'COD', _('Cash on delivery')
        PAYPAL = 'PAYPAL', _('Paypal')

    code = models.CharField(max_length=12, default=generate_code, unique=True)
    stage = models.CharField(
        max_length=32, choices=Stage.choices, default=Stage.TO_PAY)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    discount_ticket = models.ForeignKey(
        DiscountTicket, blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL)
    payment_method = models.CharField(
        max_length=16, choices=PaymentMethod.choices)

    objects = OrderManager.from_queryset(OrderQuerySet)()

    @property
    def subtotal(self) -> float:
        return sum(cart_item.amount for cart_item in self.cartitem_set.all())

    @property
    def discount(self) -> float:
        return (self.subtotal * self.discount_ticket.percent) / 100 if self.discount_ticket else None

    @property
    def amount(self) -> float:
        return self.subtotal - (self.discount or 0)

    @property
    def paid_at(self):
        return self.transaction.paid_at if self.transaction else None

    def __str__(self):
        return self.code
