from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model


class EmailUsernamePhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        identify = username or kwargs.get('identify')
        try:
            user = UserModel.objects.filter(
                Q(email=identify)
                | (Q(username__isnull=False) & Q(username=identify))
                | (Q(phone__isnull=False) & Q(phone=identify))
            ).first()
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
