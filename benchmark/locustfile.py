from locust import HttpUser, task
import random


class LoadBenchmark(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @task
    def fetch_products_and_detail(self):
        # fetch products
        random_offset = random.randint(0, 7000)
        products_res = self.client.get(
            f'/api/v1/products/?limit=10&offset={random_offset}')
        assert products_res.status_code == 200
        assert len(products_res.json()['results']) == 10

        # fetch product detail
        random_index = random.randint(0, 9)
        product_id = products_res.json()['results'][random_index]['id']
        product_detail_res = self.client.get(f'/api/v1/products/{product_id}/')
        assert product_detail_res.status_code == 200
        assert product_detail_res.json()['id'] == product_id