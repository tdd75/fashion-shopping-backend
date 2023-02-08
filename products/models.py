from django.db.models import Sum
from django.contrib.auth import get_user_model

from api.models import models, BaseModel
from .managers import ProductManager, ProductQuerySet
from product_categories.models import ProductCategory


class Product(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    feature_vector = models.TextField(null=True, default=None)
    favorited_users = models.ManyToManyField(get_user_model(), blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    objects = ProductManager.from_queryset(ProductQuerySet)()

    @property
    def review_count(self):
        return self.review_set.count()

    @property
    def rating(self):
        review_count = self.review_count
        return (self.review_set.aggregate(Sum('rating')).get('rating__sum', 0) / review_count) \
            if review_count > 0 else 0

    @property
    def price_range(self):
        product_variants = self.productvariant_set.all()
        if not product_variants:
            return None
        return (min(product_variant.price for product_variant in product_variants),
                max(product_variant.price for product_variant in product_variants))

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
