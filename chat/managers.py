from django.db.models import Q
from django.db import models


class ChatQuerySet(models.QuerySet):
    def create(self, **kwargs):
        instance = super().create(**kwargs, is_last_message=True)
        self.conversation(instance.sender.id, instance.receiver.id).exclude(
            pk=instance.id).order_by('-created_at').update(is_last_message=False)
        return instance

    def has_owned(self, user_id):
        return self.filter(Q(receiver_id=user_id) | Q(sender_id=user_id))

    def conversation(self, id1, id2):
        return self.filter(Q(receiver_id=id1, sender_id=id2) | Q(receiver_id=id2, sender_id=id1))

    def last_messages(self, staff_id):
        return self.has_owned(staff_id).filter(is_last_message=True).order_by('-created_at')


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
