from django.db import models


class ProductVariantQuerySet(models.QuerySet):
    def with_num_sold(self):
        return self.filter(cartitem__order__isnull=False).annotate(annotate_num_sold=models.Sum('cartitem__quantity'))


class ProductVariantManager(models.Manager):
    def get_color_list(self):
        return self.values_list('color', flat=True).distinct()

    def get_size_list(self):
        return self.values_list('size', flat=True).distinct()
