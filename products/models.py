from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/images/products')
    description = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0,
                                 validators=[MinValueValidator(0), MaxValueValidator(5)])
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # support fields for calculate average rating based on reviews
    rating_accumulate = models.PositiveBigIntegerField(default=0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
