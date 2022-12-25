from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .managers import CustomUserManager


class Address(models.Model):
    city = models.CharField(max_length=64)
    district = models.CharField(max_length=64)
    ward = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    detail = models.CharField(max_length=255)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email'), unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    avatar = models.ImageField(
        upload_to='static/images/users', blank=True, null=True)
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, blank=True, null=True)

    objects = CustomUserManager()

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email
