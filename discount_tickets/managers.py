from django.db import models
from django.utils import timezone


class DiscountTicketQuerySet(models.QuerySet):
    def is_unexpired(self):
        return self.filter(end_at__gte=timezone.now().isoformat())


class DiscountTicketManager(models.Manager):
    pass
