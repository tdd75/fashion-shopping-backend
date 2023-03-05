"""
WSGI config for fashion_shopping_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import debugpy

from django.core.wsgi import get_wsgi_application
from django.conf import settings


if settings.DEBUG:
    debugpy.listen(('0.0.0.0', 9999))
    debugpy.wait_for_client()


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'fashion_shopping_backend.settings')

application = get_wsgi_application()
