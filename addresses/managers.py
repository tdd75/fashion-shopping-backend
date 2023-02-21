from django.db import models


class AddressQuerySet(models.QuerySet):
    def has_owned(self, user_id):
        return self.filter(owner_id=user_id)


class AddressManager(models.Manager):
    pass