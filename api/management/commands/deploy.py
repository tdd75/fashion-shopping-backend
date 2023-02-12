import os
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Deploy with daphne'

    def handle(self, *args, **kwargs):
        os.system('daphne -b 0.0.0.0 fashion_shopping_backend.asgi:application')
