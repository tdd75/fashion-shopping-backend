from api.models import models, BaseModel
from .managers import ProductCategoryManager, ProductCategoryQuerySet


class ProductCategory(BaseModel):
    name = models.CharField(max_length=64)

    objects = ProductCategoryManager.from_queryset(ProductCategoryQuerySet)()

    def __str__(self):
        return f'{self.name}'
