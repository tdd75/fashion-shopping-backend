from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from api.models import models, BaseModel
from products.models import Product
from .managers import ReviewManager, ReviewQuerySet


class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    objects = ReviewManager.from_queryset(ReviewQuerySet)()

    def __str__(self):
        return self.content
