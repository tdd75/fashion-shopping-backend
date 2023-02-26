from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, Min, Max

from product_variants.models import ProductVariant


@receiver(post_save, sender=ProductVariant)
def update_price(sender, instance, **kwargs):
    obj = instance.product

    # min_price
    obj.min_price = obj.productvariant_set.aggregate(
        Min('price')).get('price__min', None)
    # max_price
    obj.max_price = obj.productvariant_set.aggregate(
        Max('price')).get('price__max', None)
    # rating
    review_count = obj.review_count
    if review_count == 0:
        obj.rating = 0
    else:
        obj.rating = obj.review_set.aggregate(
            Sum('rating')).get('rating__sum', 0) / review_count
    # num_sold
    obj.num_sold = obj.productvariant_set.with_num_sold().aggregate(
        Sum('annotate_num_sold')).get('annotate_num_sold__sum', 0)
    # stocks
    obj.stocks = obj.productvariant_set.aggregate(
        Sum('stocks')).get('stocks__sum', 0)

    obj.save()
