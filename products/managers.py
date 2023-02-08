from django.db import models
import requests


class ProductQuerySet(models.QuerySet):
    pass
    

class ProductManager(models.Manager):
    def calculate_feature_vector(self, product_id):
        pass

    def search_by_image(self, image_path):
        res = requests.post('http://localhost:8001/api/v1/query-image/',
                            json={'file_path': image_path})
        if res.ok:
            result_ids = res.json()['results']
            return self.filter(pk__in=result_ids)