from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


def create_users():
    admin_info = {
        'username': 'admin',
        'email': 'admin@gmail.com',
        'password': 'admin',
    }
    bot_info = {
        'username': 'bot',
        'email': 'bot@gmail.com',
        'password': 'bot',
    }

    UserModel = get_user_model()
    for info in [admin_info, bot_info]:
        # delete account if existed
        UserModel.objects.filter(
            email=info['email']).delete()
        # create new account
        UserModel.objects.create_superuser(**info)


def run_seed():
    create_users()


class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed()
        self.stdout.write('done.')
