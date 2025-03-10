import requests
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class ForgotPasswordQuerySet(models.QuerySet):
    def is_valid_record(self, email, code):
        return self.filter(
            user__email=email, code=code,
            expired_at__gte=timezone.now().isoformat()
        ).exists()


class ForgotPasswordManager(models.Manager):
    def _trigger_oauth_login(self, user_info):
        user = get_user_model().objects.filter(
            email=user_info['email']).first()
        if not user:
            user = get_user_model().objects.create(
                username=user_info['email'],
                **user_info,
            )
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
        return RefreshToken.for_user(user)

    def oauth_google(self, token):
        oauth_url = f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'
        response = requests.get(oauth_url).json()
        if response.get('error'):
            raise AuthenticationFailed('Invalid token')
        user_info = {
            'email': response['email'],
            'first_name': response['given_name'],
            'last_name': response['family_name'],
        }
        refresh = self._trigger_oauth_login(user_info)
        return refresh

    def oauth_facebook(self, token):
        oauth_url = f'https://graph.facebook.com/me?fields=first_name,last_name,email,picture&access_token={token}'
        response = requests.get(oauth_url).json()
        if response.get('error'):
            raise AuthenticationFailed('Invalid token')
        user_info = {
            'email': response['email'],
            'first_name': response['first_name'],
            'last_name': response['last_name'],
        }
        refresh = self._trigger_oauth_login(user_info)
        return refresh

    def send_otp(self, email):
        code = get_random_string(length=6, allowed_chars='0123456789')
        html_content = render_to_string(
            'email/forgot-password.html', {'code': code})

        msg = EmailMultiAlternatives(subject='Forgot password', to=[email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        self.create(code=code,
                    user=get_user_model().objects.by_email(email),
                    expired_at=timezone.now() + timezone.timedelta(minutes=settings.OTP_EXPIRE_MINUTES))
