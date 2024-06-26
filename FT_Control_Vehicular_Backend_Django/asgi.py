"""
ASGI config for FT_Control_Vehicular_Backend_Django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FT_Control_Vehicular_Backend_Django.settings')

application = get_asgi_application()
