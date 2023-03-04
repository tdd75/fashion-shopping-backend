import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Deploy with gunicorn'

    def handle(self, *args, **kwargs):
        os.system(
            'gunicorn fashion_shopping_backend.wsgi -c fashion_shopping_backend/gunicorn.conf.py & \
            daphne -b 0.0.0.0 -p 8001 fashion_shopping_backend.asgi:application')
