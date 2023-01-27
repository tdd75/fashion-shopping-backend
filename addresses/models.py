from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q, UniqueConstraint


class Address(models.Model):
    full_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=64)
    district = models.CharField(max_length=64)
    ward = models.CharField(max_length=64)
    detail = models.CharField(max_length=255)
    is_default = models.BooleanField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['is_default'], condition=Q(is_default=True), name='only_one_default_address'
            ),
        ]
