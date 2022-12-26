from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class ChatMessage(models.Model):
    content = models.TextField()
    receiver = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='receiver')
    sender = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='sender')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
