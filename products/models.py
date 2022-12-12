from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/upload/product')
    description = models.TextField()
    price = models.FloatField()
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    available = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
