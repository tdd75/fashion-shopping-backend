from django.db import models
import requests
import base64


class ProductQuerySet(models.QuerySet):
    def by_price_range(self, min_price, max_price):
        return self.filter(price__gte=min_price, price__lte=max_price)

    def with_price_range(self):
        data = self.aggregate(min_price=models.Min(
            'min_price'), max_price=models.Max('max_price'))
        return [data.get('min_price'), data.get('max_price')]


class ProductManager(models.Manager):
    def calculate_feature_vector(self, product_id):
        pass

    def search_by_image(self, encoded_string, *, exclude_ids=None):
        res = requests.post('http://image_search:8001/api/v1/query-image/',
                            json={'file': encoded_string})
        if res.ok:
            result_ids = res.json()['results']
            if exclude_ids:
                result_ids = [id for id in result_ids if id not in exclude_ids]
            return self.filter(pk__in=result_ids[:10])
