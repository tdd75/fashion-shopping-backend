"""
ASGI config for fashion_shopping_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'fashion_shopping_backend.settings')

asgi_apps = get_asgi_application()

from chat import routing
from chat.middlewares import WebSocketJWTAuthMiddleware


application = ProtocolTypeRouter(
    {
        'http': asgi_apps,
        'websocket': WebSocketJWTAuthMiddleware(URLRouter(routing.websocket_urlpatterns)),
    }
)
