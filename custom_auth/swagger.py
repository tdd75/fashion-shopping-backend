from drf_spectacular.utils import OpenApiExample

LOGIN_EXAMPLES = [
    OpenApiExample(
        'Admin account',
        value={
            'identify': 'admin',
            'password': 'admin',
        },
    ),
    OpenApiExample(
        'Customer account',
        value={
            'identify': 'tranducduy7520@gmail.com',
            'password': 'duytd123',
        },
    ),
]

REGISTER_EXAMPLES = [
    OpenApiExample(
        'Customer account',
        value={
            'email': 'tranducduy7520@gmail.com',
            'username': 'tranducduy7520',
            'phone': '0834275110',
            'password': 'duytd123',
            'first_name': 'Duy',
            'last_name': 'Tran',
        }
    ),
]

FORGOT_PASSWORD_EXAMPLES = [
    OpenApiExample(
        'Customer account',
        value={
            'email': 'tranducduy7520@gmail.com',
        }
    ),
]
