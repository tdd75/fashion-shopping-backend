from django.db import models


class CartQuerySet(models.QuerySet):
    def has_owned(self, user_id):
        return self.filter(owner_id=user_id)

    def is_ordered(self, value):
        return self.filter(order__isnull=not value)

    def by_product_variant_id(self, id):
        return self.filter(product_variant_id=id).first()

    def with_amount(self):
        return self.annotate(annotate_amount=models.F('product_variant__price') * models.F('quantity'))


class CartManager(models.Manager):
    pass
