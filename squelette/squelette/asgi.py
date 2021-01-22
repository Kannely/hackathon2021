"""
ASGI config for squelette project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

import importlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'squelette.settings')

is_scalingo = importlib.util.find_spec("dj_static")
if is_scalingo is not None:
    print("Using Cling...")
    from dj_static import Cling
    application = Cling(get_asgi_application())
else:
    application = get_asgi_application()
