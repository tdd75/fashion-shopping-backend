from multiprocessing import cpu_count

bind = '0.0.0.0:8000'
workers = cpu_count() * 2 + 1
# daemon = True
# worker_class = 'gevent'
# max_requests = 1000
