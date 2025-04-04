# from stellarfinder.settings.settings import *
from .settings import *

DEBUG = False


# Collect static files for production
STATIC_ROOT = BASE_DIR / 'static'

# Security settings for production
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
