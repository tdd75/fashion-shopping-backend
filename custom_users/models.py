from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email'), unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    objects = CustomUserManager()

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email
