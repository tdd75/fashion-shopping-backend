from django.contrib.auth import get_user_model
from django.db.models import Q, UniqueConstraint

from api.models import models, BaseModel
from .managers import AddressManager, AddressQuerySet


class Address(BaseModel):
    full_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=64)
    district = models.CharField(max_length=64)
    ward = models.CharField(max_length=64)
    detail = models.CharField(max_length=255)
    is_default = models.BooleanField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    objects = AddressManager.from_queryset(AddressQuerySet)()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['is_default'], condition=Q(is_default=True), name='only_one_default_address'
            ),
        ]
