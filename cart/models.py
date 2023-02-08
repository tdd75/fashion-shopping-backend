from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from api.models import models, BaseModel
from product_variants.models import ProductVariant
from orders.models import Order
from .managers import CartManager, CartQuerySet


class CartItem(BaseModel):
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    product_variant = models.ForeignKey(
        ProductVariant, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    objects = CartManager.from_queryset(CartQuerySet)()

    @property
    def amount(self) -> float:
        return self.product_variant.price * self.quantity

    def __str__(self):
        return f'{self.product_variant}_{self.quantity}'
