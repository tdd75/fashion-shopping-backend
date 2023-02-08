
import os
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Deploy with gunicorn'

    def handle(self, *args, **kwargs):
        os.system(
            'find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
