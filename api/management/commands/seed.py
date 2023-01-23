from django.core.management.base import BaseCommand

from .seeder.user import create_users
from .seeder.product import create_products


class Command(BaseCommand):
    help = "Seed database for testing and development"

    def handle(self, *args, **options):
        self.stdout.write('###Start')

        self.stdout.write('Seeding users...')
        create_users()
        self.stdout.write('Done seeding users')

        self.stdout.write('Seeding products...')
        create_products()
        self.stdout.write('Done seeding products')

        self.stdout.write('###End')
