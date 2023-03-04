from locust import HttpUser, task


class LoadBenchmark(HttpUser):
    @task
    def fetch_products(self):
        res = self.client.get('/api/v1/products/?limit=10', headers={
            # 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4Mzg1Mjg5LCJpYXQiOjE2Nzc3ODA0ODksImp0aSI6ImIxODkyYzIwOTJiZDQ2ZDdiYTg3ZmU5MjMyMjE0MTBmIiwidXNlcl9pZCI6MTl9.2FI9uITDUjsfVXkSuh0pLJGNexmKkEEgcWffuM7j-8c'
        })
        print(res.json())
        assert res.status_code == 200

    # @task
    # def login(self):
    #     res = self.client.post('/user/login', json={
    #         'Username': 'tuannha',
    #         'Password': '123456',
    #         'Role': 1
    #     })
    #     print(res.json())
    #     assert res.status_code == 200
