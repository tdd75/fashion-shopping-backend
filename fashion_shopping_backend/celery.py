import os
import requests
from datetime import timedelta
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'fashion_shopping_backend.settings')

app = Celery('fashion_shopping')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def calculate_product_vector(self, id):
    from products.models import Product
    product = Product.objects.filter(pk=id)
    # requests.post('http://localhost:8001/api/v1/products/1/get-vector/',
    #               data={'file_path': 'products/1/1.jpg'})
    # product.update(feature_vector='[1, 2, 3]')


@app.task(bind=True, name='update_product_vector')
def update_product_vector(self):
    from products.models import Product

    for product in Product.objects.filter(feature_vector__isnull=True)[:10]:
        print(product.image.url)
        res = requests.post('http://localhost:8001/api/v1/get-vector/',
                            json={'file_path': product.image.url})
        if res.ok:
            product.feature_vector = res.json()['vector']
            product.save()


# cron jobs
app.conf.beat_schedule = {
    'calculate-feature-vector': {
        'task': 'update_product_vector',
        'schedule': timedelta(seconds=5),
    },
}
