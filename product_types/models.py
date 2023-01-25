from django.db import models
from django.core.validators import MinValueValidator

from products.models import Product


class ProductType(models.Model):
    color = models.CharField(max_length=32)
    size = models.CharField(max_length=16)
    stocks = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('color', 'size', 'product',)

    def __str__(self):
        return f'{self.color}_{self.size}'
