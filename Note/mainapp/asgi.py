"""
ASGI config for Note project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import logging

# Logging 
logger = logging.getLogger(__name__)

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Note.settings')

application = get_asgi_application()
logger.info('ASGI application created.')
