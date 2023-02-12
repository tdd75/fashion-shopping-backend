from django.db.models import Sum, Min, Max
from django.contrib.auth import get_user_model
from computedfields.models import ComputedFieldsModel, computed, compute

from api.models import models, BaseModel
from .managers import ProductManager, ProductQuerySet
from product_categories.models import ProductCategory


class Product(BaseModel, ComputedFieldsModel):
    objects = ProductManager.from_queryset(ProductQuerySet)()

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    feature_vector = models.TextField(null=True, default=None)
    favorited_users = models.ManyToManyField(get_user_model(), blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    @computed(models.DecimalField(max_digits=12, decimal_places=2, null=True, default=None),
              depends=[('productvariant_set', ['price'])])
    def min_price(self):
        if not self.pk:
            return None
        return self.productvariant_set.aggregate(Min('price')).get('price__min', None)

    @computed(models.DecimalField(max_digits=12, decimal_places=2, null=True, default=None),
              depends=[('productvariant_set', ['price'])])
    def max_price(self):
        if not self.pk:
            return None
        return self.productvariant_set.aggregate(Max('price')).get('price__max', None)

    @computed(models.PositiveIntegerField(), depends=[('review_set', [])])
    def review_count(self):
        return self.review_set.count()

    @computed(models.DecimalField(max_digits=2, decimal_places=1), depends=[('review_set', ['rating'])])
    def rating(self):
        review_count = self.review_count
        if review_count == 0:
            return 0
        return (self.review_set.aggregate(Sum('rating')).get('rating__sum', 0) / review_count)

    @property
    def price_range(self):
        return (self.min_price, self.max_price)

    @property
    def stocks(self):
        return sum(product_variant.stocks for product_variant in self.productvariant_set.all())

    def update_is_favorite(self, user_id, new_value):
        if new_value:
            self.favorited_users.add(user_id)
        else:
            self.favorited_users.remove(user_id)
            
    # @property
    # def num_sold(self):
    #     review_count = self.review_set.count()
    #     return (self.review_set.aggregate(Sum('rating')).get('rating__sum', 0) / review_count) \
    #         if review_count > 0 else 0

    def __str__(self):
        return self.name
