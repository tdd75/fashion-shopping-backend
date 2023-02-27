from django.db import models
import requests


class ChatQuerySet(models.QuerySet):
    def create(self, **kwargs):
        instance = super().create(**kwargs, is_last_message=True)
        self.conversation(instance.sender.id, instance.receiver.id).exclude(
            pk=instance.id).order_by('-created_at').update(is_last_message=False)
        return instance

    def has_owned(self, user_id):
        return self.filter(models.Q(receiver_id=user_id) | models. Q(sender_id=user_id))

    def conversation(self, id1, id2):
        return self.filter(models.Q(receiver_id=id1, sender_id=id2) | models.Q(receiver_id=id2, sender_id=id1))

    def last_messages(self, staff_id):
        return self.has_owned(staff_id).filter(is_last_message=True).order_by('-created_at')


class ChatManager(models.Manager):
    def call_rasa(self, message):
        res = requests.post('http://chatbot:5005/webhooks/rest/webhook', json={
            'message': message,
        })
        if res.ok:
            return res.json()
        else:
            return None
        # msg = ChatMessage.objects.create(user=request.user, message={
        #                              "message": request.data["message"]})
        # socket_message = f"Message with id {msg.id} was created!"
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     f"{request.user.id}-message", {"type": "send_last_message",
        #                                    "text": socket_message}
        # )

    def process_msg(self, request, msg, init_chatbot_at):
        custom_msg = msg.get('custom')
        if not custom_msg:
            return msg

        # get data from API
        headers = {
            'Authorization': f'Bearer {request.auth.token.decode("utf-8")}'
        }
        if custom_msg['payload'] == 'list_product':
            res = requests.get(
                'http://localhost:8000/api/v1/products/', headers=headers, params={
                    **custom_msg['data'],
                    'limit': 5,
                })
        elif custom_msg['payload'] == 'order_status':
            res = requests.get(
                'http://localhost:8000/api/v1/orders/', headers=headers, params={
                    'ordering': '-updated_at',
                    'expand': 'order_items,order_items.product_variant,order_items.product_variant.product',
                    'limit': 5,
                })
        elif custom_msg['payload'] == 'place_order':
            res = requests.get(
                'http://localhost:8000/api/v1/cart/', headers=headers, params={
                    'ordering': '-updated_at',
                    'expand': 'product_variant,product_variant.product',
                    'updated_at': init_chatbot_at,
                })
        # fill data for custom message
        if not res.ok or not res.json()['results']:
            return None
        msg['custom']['data'] = res.json()['results']

        return msg
