import os
import requests
from datetime import timedelta
from celery import Celery

from fashion_shopping_backend.helpers import convert_to_base64

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'fashion_shopping_backend.settings')

app = Celery('fashion_shopping')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


def _calculate_product_vector(product):
    res = requests.post('http://image_search:8001/api/v1/get-vector/',
                        json={'file': convert_to_base64(product.image)})
    if res.ok:
        product.feature_vector = res.json()['vector']
        product.save()


@app.task(bind=True)
def calculate_product_vector(self, id):
    from products.models import Product
    product = Product.objects.filter(pk=id)
    _calculate_product_vector(product)


@app.task(bind=True)
def test_task(self):
    print(123)


@app.task(bind=True, name='update_product_vector')
def update_product_vector(self):
    from products.models import Product

    for product in Product.objects.filter(feature_vector__isnull=True)[:500]:
        _calculate_product_vector(product)


# cron jobs
app.conf.beat_schedule = {
    'calculate-feature-vector': {
        'task': 'update_product_vector',
        'schedule': timedelta(minutes=5),
    },
}
