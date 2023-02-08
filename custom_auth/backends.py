from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth import get_user_model


class EmailUsernamePhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        identify = username or kwargs.get('identify')
        user = User.objects.filter(
            Q(email=identify)
            | (Q(username__isnull=False) & Q(username=identify))
            | (Q(phone__isnull=False) & Q(phone=identify))
        ).first()
        if not user:
            raise ValidationError('User not found')

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
