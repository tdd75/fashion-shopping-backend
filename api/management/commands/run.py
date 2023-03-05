import os
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Deploy with gunicorn'

    def handle(self, *args, **kwargs):
        run_command = 'gunicorn fashion_shopping_backend.wsgi -c fashion_shopping_backend/gunicorn.conf.py'
        
        if settings.DEBUG:
            run_command += ' -w 1'
        
        os.system(run_command)