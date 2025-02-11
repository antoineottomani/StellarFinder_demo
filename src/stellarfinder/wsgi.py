import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'stellarfinder.settings.demo_production')

application = get_wsgi_application()
