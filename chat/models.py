from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from api.models import models, BaseModel
from .managers import ChatManager, ChatQuerySet


class ChatMessage(BaseModel):
    content = models.TextField()
    receiver = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='receiver')
    sender = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='sender')
    is_last_message = models.BooleanField(default=False)

    objects = ChatManager.from_queryset(ChatQuerySet)()

    def __str__(self):
        return self.content
