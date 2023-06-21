from django.contrib import admin
from .models import Note, Group
import logging

# Logging 
logger = logging.getLogger(__name__)

admin.site.register(Note)
logger.info('Note registered.')

admin.site.register(Group)
logger.info('Group registered.')


