from django.utils import timezone
import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _


class DiscountTicket(models.Model):
    class DiscountType(models.TextChoices):
        RAW_VALUE = 'RAW_VALUE', _('Raw value')
        PERCENT = 'PERCENT', _('Percent')

    type = models.CharField(
        max_length=16, choices=DiscountType.choices, default=DiscountType.RAW_VALUE)
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    min_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    def __str__(self):
        if self.type == self.DiscountType.RAW_VALUE:
            return f'-{self.value}_min_order_{self.min_amount}'
        else:
            return f'{self.value}%_min_order_{self.min_amount}'
