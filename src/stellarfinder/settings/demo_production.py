from stellarfinder.settings.settings import *

DEBUG = False

# Define the allowed hosts for the production environment
ALLOWED_HOSTS = [
    "stellarfinder.ovh",
    "www.stellarfinder.ovh",
    "stellarfinder-env.eba-ywazt47c.eu-west-3.elasticbeanstalk.com",
]

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
