from django.db.models import Sum, Min, Max
from django.contrib.auth import get_user_model

from api.models import models, BaseModel
from .managers import ProductManager, ProductQuerySet
from product_categories.models import ProductCategory


class Product(BaseModel):
    objects = ProductManager.from_queryset(ProductQuerySet)()

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    favorited_users = models.ManyToManyField(get_user_model(), blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    feature_vector = models.TextField(null=True, default=None)

    @property
    def min_price(self):
        return self.productvariant_set.aggregate(Min('price')).get('price__min', None)

    @property
    def max_price(self):
        return self.productvariant_set.aggregate(Max('price')).get('price__max', None)

    @property
    def price_range(self):
        return [self.min_price, self.max_price]

    @property
    def review_count(self):
        return self.review_set.count()

    @property
    def rating(self):
        review_count = self.review_count
        if review_count == 0:
            return 0
        return self.review_set.aggregate(Sum('rating')).get('rating__sum', 0) / review_count

    @property
    def num_sold(self):
        return self.productvariant_set.with_num_sold().aggregate(Sum('annotate_num_sold')).get('annotate_num_sold__sum', 0)

    @property
    def stocks(self):
        return self.productvariant_set.aggregate(Sum('stocks')).get('stocks__sum', 0)

    def update_is_favorite(self, user_id, new_value):
        if new_value == True:
            self.favorited_users.add(user_id)
        elif new_value == False:
            self.favorited_users.remove(user_id)

    def __str__(self):
        return self.name
