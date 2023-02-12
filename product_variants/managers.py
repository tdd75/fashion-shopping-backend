from django.db import models


class ProductVariantQuerySet(models.QuerySet):
    def get_color_list(self):
        return self.values_list('color', flat=True).distinct()
    
    def get_size_list(self):
        return self.values_list('size', flat=True).distinct()


class ProductVariantManager(models.Manager):
    pass
