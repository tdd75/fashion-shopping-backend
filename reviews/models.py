from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from api.models import models, BaseModel
from product_variants.models import ProductVariant
from products.models import Product
from orders.models import Order
from .managers import ReviewManager, ReviewQuerySet


class Review(BaseModel):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    objects = ReviewManager.from_queryset(ReviewQuerySet)()

    def __str__(self):
        return self.content
