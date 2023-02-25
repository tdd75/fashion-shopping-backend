from django.conf import settings
import firebase_admin
from firebase_admin import credentials, messaging


class FirebaseService:
    def __init__(self) -> None:
        cred = credentials.Certificate(
            'fashion_shopping_backend/services/fashion-shopping-366319-firebase-adminsdk-u6ytp-e4487932fb.json')
        firebase_admin.initialize_app(cred)

    def send_notification(self):
        message = messaging.Message(
            topic='discount',
            notification=messaging.Notification(
                title='Discount',
                body='We have some new discount tickets. Let\'s check it now.',
                image='https://e7.pngegg.com/pngimages/824/405/png-clipart-discount-tickets-logo-discounts-and-allowances-cheaptickets-gift-card-hotel-cheaptickets-label-text.png',
            ),
            data={
                'route': '/discount-ticket'
            },
        )
        messaging.send(message)


firebase_service = FirebaseService()
