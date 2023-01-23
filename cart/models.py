from django.db import models
from django.contrib.auth import get_user_model

from orders.models import Order
from products.models import Product
from product_types.models import ProductType



class CartItem(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL)
    product_type = models.ForeignKey(
        ProductType, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, null=True, default=None, on_delete=models.CASCADE)

    # # backup product information fields
    # name = models.CharField(max_length=255)
    # size = models.CharField(max_length=16)
    # color = models.CharField(max_length=32)
    # image = models.URLField()
    # price = models.DecimalField(
    #     max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    @property
    def amount(self):
        return self.price * self.quantity

    class Meta:
        indexes = (
            models.Index(fields=('order',)),
        )

    def __str__(self):
        return f'{self.product_type}_{self.quantity}'
