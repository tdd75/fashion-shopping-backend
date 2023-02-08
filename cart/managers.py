from django.db import models


class CartQuerySet(models.QuerySet):
    def has_owned(self, user_id):
        return self.filter(owner_id=user_id)

    def is_ordered(self, value):
        return self.filter(order__isnull=not value)

    def get_by_product_variant_id(self, id):
        return self.filter(product_variant_id=id).first()


class CartManager(models.Manager):
    pass
