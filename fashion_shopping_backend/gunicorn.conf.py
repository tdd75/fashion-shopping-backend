from multiprocessing import cpu_count

bind = '127.0.0.1:8000'
workers = cpu_count() * 2 + 1
# daemon = True
# worker_class = 'gevent'
# max_requests = 1000
