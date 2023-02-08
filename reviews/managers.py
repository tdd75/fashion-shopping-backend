from django.db import models


class ReviewQuerySet(models.QuerySet):
    def has_owned(self, user_id):
        return self.filter(owner_id=user_id)


class ReviewManager(models.Manager):
    pass
