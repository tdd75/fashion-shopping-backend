from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    feature_vector = models.BinaryField(null=True, default=None)
    favorited_users = models.ManyToManyField(get_user_model(), blank=True)

    @property
    def rating(self):
        review_count = self.review_set.count()
        return (self.review_set.aggregate(Sum('rating')).get('rating__sum', 0) / review_count) \
            if review_count > 0 else 0

    @property
    def price_range(self):
        product_types = self.producttype_set.all()
        if not product_types:
            return None
        return (min(product_type.price for product_type in product_types),
                max(product_type.price for product_type in product_types))

    @property
    def stocks(self):
        return sum(product_type.stocks for product_type in self.producttype_set.all())

    def __str__(self):
        return self.name
