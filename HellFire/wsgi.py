"""
WSGI config for HellFire project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HellFire.settings')
application = get_wsgi_application()
