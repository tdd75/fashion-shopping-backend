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
    # computed fields
    min_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, default=None)
    max_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, default=None)
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, default=None)
    num_sold = models.PositiveIntegerField(null=True, default=None)
    stocks = models.PositiveIntegerField(null=True, default=None)

    @property
    def price_range(self):
        return [self.min_price, self.max_price]

    @property
    def review_count(self):
        return self.review_set.count()

    def update_is_favorite(self, user_id, new_value):
        if new_value == True:
            self.favorited_users.add(user_id)
        elif new_value == False:
            self.favorited_users.remove(user_id)

    def __str__(self):
        return self.name
