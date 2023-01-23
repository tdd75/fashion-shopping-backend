from django.contrib.auth import get_user_model


def create_users():
    User = get_user_model()
    User.objects.all().delete()

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
    for info in [admin_info, bot_info]:
        User.objects.create_superuser(**info)
