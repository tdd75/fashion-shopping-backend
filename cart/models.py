from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from product_types.models import ProductType


class CartItem(models.Model):
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    product_type = models.ForeignKey(
        ProductType, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_type}_{self.quantity}'

    class Meta:
        unique_together = ('product_type', 'owner',)
