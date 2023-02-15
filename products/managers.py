from django.db import models
import requests
import base64


class ProductQuerySet(models.QuerySet):
    def with_min_price(self):
        return self.annotate(annotate_min_price=models.Min('productvariant__price'))

    def with_max_price(self):
        return self.annotate(annotate_max_price=models.Max('productvariant__price'))


class ProductManager(models.Manager):
    def calculate_feature_vector(self, product_id):
        pass

    def search_by_image(self, encoded_string, *, exclude_ids=None):
        res = requests.post('http://image_search:8001/api/v1/query-image/',
                            json={'file': encoded_string})
        if not res.ok:
            return []
        result_ids = res.json()['results']
        if exclude_ids:
            result_ids = [id for id in result_ids if id not in exclude_ids]
        return self.filter(pk__in=result_ids[:10])

    def get_price_range(self):
        data = self.aggregate(min_price=models.Min(
            'productvariant__price'), max_price=models.Max('productvariant__price'))
        return [data.get('min_price'), data.get('max_price')]
