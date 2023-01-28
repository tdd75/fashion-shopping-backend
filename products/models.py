from django.db.models import Sum
from django.contrib.auth import get_user_model

from api.models import models, BaseModel
from .managers import ProductManager


class Product(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    feature_vector = models.BinaryField(null=True, default=None)
    favorited_users = models.ManyToManyField(get_user_model(), blank=True)

    objects = ProductManager()

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

    def update_is_favorite(self, user_id, new_value):
        if new_value:
            self.favorited_users.add(user_id)
        else:
            self.favorited_users.remove(user_id)

    def __str__(self):
        return self.name
