from django.db import models


class OrderQuerySet(models.QuerySet):
    def has_owned(self, user_id):
        return self.filter(owner_id=user_id)


class OrderManager(models.Manager):
    def clean_items_in_cart(self):
        pass
    