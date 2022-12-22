from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product
from product_types.models import ProductType


class CartItem(models.Model):
    image = models.URLField()
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
