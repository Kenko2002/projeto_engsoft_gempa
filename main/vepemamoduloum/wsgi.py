"""
WSGI config for gs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('S_MODULE', 'vepemamoduloum.settings.local')

application = get_wsgi_application()
