from stellarfinder.settings.settings import *

DEBUG = False

# Define the allowed hosts for the production environment
ALLOWED_HOSTS = env("ALLOWED_HOSTS", "").split(",")

# Collect static files for production
STATIC_ROOT = BASE_DIR / 'static'

# Security settings for production
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
