from django.db.models import Q
from django.db import models


class ChatQuerySet(models.QuerySet):
    def has_owned(self, user_id):
        return self.filter(Q(receiver_id=user_id) | Q(sender_id=user_id))


class ChatManager(models.Manager):
    pass
    # def send_message(self):
    #     msg = ChatMessage.objects.create(user=request.user, message={
    #                                  "message": request.data["message"]})
    #     socket_message = f"Message with id {msg.id} was created!"
    #     channel_layer = get_channel_layer()
    #     async_to_sync(channel_layer.group_send)(
    #         f"{request.user.id}-message", {"type": "send_last_message",
    #                                        "text": socket_message}
    #     )
