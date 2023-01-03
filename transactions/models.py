from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


from orders.models import Order


class Transaction(models.Model):
    amount = models.CharField(max_length=32)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.order.code}_{self.amount}'
