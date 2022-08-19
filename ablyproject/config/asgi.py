"""
ASGI config for ablyproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from config.utils import get_config_value


if get_config_value("ACCESS_TYPE") == "dev":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ablyproject.config.settings.dev')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ablyproject.config.settings.service')

application = get_asgi_application()
