from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from api.models import models, BaseModel
from product_types.models import ProductType
from .managers import CartManager, CartQuerySet


class CartItem(BaseModel):
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    product_type = models.ForeignKey(
        ProductType, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    objects = CartManager.from_queryset(CartQuerySet)()

    @property
    def is_ordered(self):
        return self.order_set is not None

    def __str__(self):
        return f'{self.product_type}_{self.quantity}'
