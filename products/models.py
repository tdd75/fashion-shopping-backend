from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/images/products')
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # supported fields for calculate average rating based on reviews
    rating_accumulate = models.PositiveBigIntegerField(default=0)
    rating_count = models.IntegerField(default=0)

    @property
    def rating(self) -> float:
        if self.rating_count == 0:
            return 0
        return self.rating_accumulate / self.rating_count

    def __str__(self):
        return self.name
