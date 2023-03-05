from multiprocessing import cpu_count

bind = '0.0.0.0:8001'
workers = 2
worker_class = 'uvicorn.workers.UvicornWorker'
# daemon = True
# max_requests = 1000
