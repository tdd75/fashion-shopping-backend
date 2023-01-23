from locust import HttpUser, task


class LoadBenchmark(HttpUser):
    # @task
    # def fetch_products(self):
    #     res = self.client.get("/api/v1/products/?limit=10", headers={
    #         'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc0MzE1NDgwLCJpYXQiOjE2NzM3MTA2ODAsImp0aSI6IjQ3ZDIwZjBkYWYwYzQzNzA5NTAxYmRhOTJhNDJmMGRkIiwidXNlcl9pZCI6M30.pzx5ZXqPDNne9rMSCTTVRImcypTYvBQp9wzISvNtySA'
    #     })
    #     assert res.status_code == 200

    @task
    def fetch_long(self):
        res = self.client.get('/admin/api/v1/news?filter=category_entity_id.1&limit=10&offset=1', headers={
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzM4MDE1MzQsImlhdCI6MTY3MzcxNTEzNCwicm9sZSI6IkFETUlOX1JPTEUiLCJ1c2VySWQiOiIxIn0.XIfWbm390j-X7CYHIekAuUDsNva-ltO44wjsrUbrOa0'
        })
        assert res.status_code == 200
