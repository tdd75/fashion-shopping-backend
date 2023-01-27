from django.utils.crypto import get_random_string


CODE_LENGTH = 8
RANDOM_STRING_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def generate_code():
    return get_random_string(CODE_LENGTH, allowed_chars=RANDOM_STRING_CHARS)
