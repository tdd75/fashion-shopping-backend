import os
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Deploy with gunicorn'

    def handle(self, *args, **kwargs):
        os.system(
            'gunicorn fashion_shopping_backend.wsgi -c fashion_shopping_backend/gunicorn.conf.py')
