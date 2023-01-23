from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model

CODE_LENGTH = 8
RANDOM_STRING_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def generate_code():
    return get_random_string(CODE_LENGTH, allowed_chars=RANDOM_STRING_CHARS)


class Order(models.Model):
    class Stage(models.TextChoices):
        TO_PAY = 'TO_PAY', _('To pay')
        TO_SHIP = 'TO_SHIP', _('To ship')
        TO_RECEIVE = 'TO_RECEIVE', _('To receive')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')

    code = models.CharField(max_length=CODE_LENGTH,
                            unique=True, default=generate_code)
    stage = models.CharField(
        max_length=32, choices=Stage.choices, default=Stage.TO_PAY)
    # order_items = models.JSONField()
    # address = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @property
    def amount(self):
        return sum(cart_item.amount for cart_item in self.cartitem_set.all())

    def __str__(self):
        return self.code


# class OrderItem(models.Model):
#     size = models.CharField(max_length=16)
#     color = models.CharField(max_length=32)
#     quantity = models.PositiveIntegerField()
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         Product, null=True, on_delete=models.SET_NULL)

#     # backup product information fields
#     image = models.URLField()
#     price = models.DecimalField(
#         max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

#     def __str__(self):
#         return f'{self.order.code}_{self.product.name}_{self.size}_{self.color}'
