import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'stellarfinder.settings.demo_production')

# Check if the environment variable is set in production
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    raise RuntimeError(
        "DJANGO_SETTINGS_MODULE is not set! Make sure to configure it.")


application = get_wsgi_application()
