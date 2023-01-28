from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint, Q
from django.utils.translation import gettext as _

from api.models import models, BaseModel
from .managers import CustomUserManager, CustomUserQuerySet


class CustomUser(BaseModel, AbstractUser):
    email = models.EmailField(_('email'))
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    objects = CustomUserManager.from_queryset(CustomUserQuerySet)()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('email',),
                condition=Q(deleted__isnull=True),
                name='unique_email'
            ),
        ]

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    def change_password(self, new_password):
        self.set_password(new_password)
        self.save()

    def __str__(self):
        return self.email
