from django.contrib.auth import get_user_model


def create_users():
    User = get_user_model()
    User.objects.all().delete()

    admin_info = {
        'username': 'admin',
        'first_name': 'Admin',
        'email': 'admin@gmail.com',
        'password': 'admin',
    }
    bot_info = {
        'username': 'bot',
        'first_name': 'Bot',
        'email': 'bot@gmail.com',
        'password': 'bot',
    }
    for info in [admin_info, bot_info]:
        User.objects.create_superuser(**info)
