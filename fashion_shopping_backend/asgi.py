"""
ASGI config for fashion_shopping_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""


import os
import debugpy

from django.core.asgi import get_asgi_application
from django.conf import settings


def get_application():
    from channels.routing import ProtocolTypeRouter, URLRouter
    from chat import routing
    from chat.middlewares import WebSocketJWTAuthMiddleware

    return ProtocolTypeRouter({
        'websocket': WebSocketJWTAuthMiddleware(URLRouter(routing.websocket_urlpatterns)),
    })


if settings.DEBUG:
    debugpy.listen(('0.0.0.0', 10000))
    debugpy.wait_for_client()

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'fashion_shopping_backend.settings')

asgi_apps = get_asgi_application()
application = get_application()
