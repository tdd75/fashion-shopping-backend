from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ParseError, AuthenticationFailed, ValidationError
import requests

from .models import ForgotPasswordCode


def _oauth(user_info: dict):
    user_existed = get_user_model().objects.filter(
        email=user_info['email']).first()
    if not user_existed:
        user = get_user_model().objects.create(
            username=user_info['email'],
            **user_info,
        )
    else:
        user = user_existed
    if api_settings.UPDATE_LAST_LOGIN:
        update_last_login(None, user)
    return RefreshToken.for_user(user)


def oauth_google(*, token: str, **kwargs) -> dict:
    oauth_url = f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'
    response = requests.get(oauth_url)
    data = response.json()
    if data.get('error'):
        raise AuthenticationFailed('Invalid token')
    user_info = {
        'email': data['email'],
        'first_name': data['given_name'],
        'last_name': data['family_name'],
    }
    refresh = _oauth(user_info)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def oauth_facebook(*, token: str, **kwargs):
    oauth_url = 'https://graph.facebook.com/me?fields='
    f'first_name,last_name,email,picture&access_token={token}'
    response = requests.get(oauth_url)
    data = response.json()
    if data.get('error'):
        raise AuthenticationFailed('Invalid token')
    user_info = {
        'email': data['email'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
    }
    refresh = _oauth(user_info)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def register(*, email: str, username: str, password: str, **kwargs):
    user = get_user_model().objects.filter(
        Q(email=email) | Q(username=username)).first()
    if not user:
        user = get_user_model().objects.create(email=email, username=username)
    elif user.password:
        raise ValidationError(f'Email or username is already in use')
    user.set_password(password)
    user.save()


def change_password(*, user: get_user_model(), old_password: str, new_password: str, **kwargs):
    if not user.check_password(old_password):
        raise ParseError({'old_password': 'Wrong password'})
    user.set_password(new_password)
    user.save()


def send_forgot_password_code(*, email: str, **kwargs):
    UserModel = get_user_model()
    user = UserModel.objects.filter(email=email).first()
    if not user:
        raise ParseError({'email': 'This email is not registered'})
    code = get_random_string(length=6, allowed_chars='0123456789')
    send_mail(f'Forgot password', f'{code}', None,
              [email], fail_silently=False)
    ForgotPasswordCode.objects.create(user=user, code=code, expired_at=timezone.now() +
                                      timezone.timedelta(minutes=settings.FORGOT_PASSWORD_CODE_EXPIRE_MINUTES))


def verify_code(*, email: str, code: str, **kwargs):
    instance = ForgotPasswordCode.objects.filter(
        user__email=email, code=code,
        expired_at__gte=timezone.now().isoformat()).first()
    if not instance:
        raise ParseError({'code': 'Code invalid'})


def recover_password(*, email: str, new_password: str, **kwargs):
    user = get_user_model().objects.filter(email=email).first()
    user.set_password(new_password)
    user.save()
