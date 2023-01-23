from django.db import models
from django.contrib.auth import get_user_model


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    feature_vector = models.BinaryField(null=True, default=None)

    # supported fields for calculate average rating based on reviews
    rating_accumulate = models.PositiveBigIntegerField(default=0)
    rating_count = models.IntegerField(default=0)

    @property
    def rating(self):
        if self.rating_count == 0:
            return 0
        return self.rating_accumulate / self.rating_count

    @property
    def price_range(self):
        product_types = self.producttype_set.all()
        if not product_types:
            return None
        return (min(product_type.price for product_type in product_types),
                max(product_type.price for product_type in product_types))

    @property
    def quantity(self):
        return sum(product_type.quantity for product_type in self.producttype_set.all())

    def __str__(self):
        return self.name
