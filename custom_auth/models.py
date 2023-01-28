from django.contrib.auth import get_user_model

from api.models import models, BaseModel
from .managers import ForgotPasswordManager, ForgotPasswordQuerySet


class ForgotPasswordCode(BaseModel):
    code = models.CharField(max_length=10)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    objects = ForgotPasswordManager.from_queryset(ForgotPasswordQuerySet)()

    def __str__(self):
        return f'{self.code}_{self.user.email}'
