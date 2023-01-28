from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

from api.models import models, BaseModel
from orders.models import Order
from .managers import TransactionManager, TransactionQuerySet


class Transaction(BaseModel):
    amount = models.CharField(max_length=32)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    objects = TransactionManager.from_queryset(TransactionQuerySet)()

    def __str__(self):
        return f'{self.order.code}_{self.amount}'
