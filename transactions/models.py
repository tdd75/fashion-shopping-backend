from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from api.models import models, BaseModel
from orders.models import Order
from .managers import TransactionManager, TransactionQuerySet


class Transaction(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_link = models.URLField()
    check_payment_link = models.URLField()
    paid_amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], null=True, default=None)
    paid_at = models.DateTimeField(null=True, default=None)

    objects = TransactionManager.from_queryset(TransactionQuerySet)()

    def __str__(self):
        return f'{self.order.code}'
