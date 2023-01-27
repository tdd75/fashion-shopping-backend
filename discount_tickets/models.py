from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class DiscountTicket(models.Model):
    class DiscountType(models.TextChoices):
        RAW_VALUE = 'RAW_VALUE', _('Raw value')
        PERCENT = 'PERCENT', _('Percent')

    type = models.CharField(
        max_length=16, choices=DiscountType.choices, default=DiscountType.RAW_VALUE)
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    min_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField()
    saved_users = models.ManyToManyField(get_user_model(), blank=True)
