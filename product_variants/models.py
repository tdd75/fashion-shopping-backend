from django.core.validators import MinValueValidator

from api.models import models, BaseModel
from products.models import Product
from .managers import ProductVariantManager, ProductVariantQuerySet


class ProductVariant(BaseModel):
    objects = ProductVariantManager.from_queryset(ProductVariantQuerySet)()

    color = models.CharField(max_length=32)
    size = models.CharField(max_length=16)
    stocks = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('color', 'size', 'product',)

    def __str__(self):
        return f'{self.color}_{self.size}'
