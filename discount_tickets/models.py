from django.db.models import Q, F
from django.db.models.functions import Now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from api.models import models, BaseModel
from .managers import DiscountTicketManager, DiscountTicketQuerySet


class DiscountTicket(BaseModel):
    percent = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)])
    min_amount = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True)
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField()
    saved_users = models.ManyToManyField(
        get_user_model(), through='TicketUserRel', blank=True)

    objects = DiscountTicketManager.from_queryset(DiscountTicketQuerySet)()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(start_at__lte=F('end_at'),
                        start_at__gte=Now()),
                name='correct_datetime'
            ),
        ]


class TicketUserRel(BaseModel):
    discount_ticket = models.ForeignKey(
        DiscountTicket, on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
