from django.db import models
from django.contrib.auth import get_user_model


class Address(models.Model):
    full_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    city = models.CharField(max_length=64)
    district = models.CharField(max_length=64)
    ward = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    detail = models.CharField(max_length=255)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
