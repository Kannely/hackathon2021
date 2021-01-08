"""
WSGI config for squelette project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

import importlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'squelette.settings')

is_scalingo = importlib.util.find_spec("dj_static")
if is_scalingo is not None:
    print("Using Cling...")
    from dj_static import Cling
    application = Cling(get_wsgi_application())
else:
    application = get_wsgi_application()
