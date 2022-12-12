from django.db import models

from products.models import Product


class ProductType(models.Model):
    color = models.CharField(max_length=32)
    size = models.CharField(max_length=16)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.color}_{self.size}'
