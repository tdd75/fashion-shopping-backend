from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class ForgotPasswordCode(models.Model):
    code = models.CharField(max_length=10)
    expired_at = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(minutes=5))
    verify_failed_count = models.PositiveIntegerField(default=0)
    recover_token = models.CharField(max_length=16, null=True, default=None)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code}_{self.user.email}'
