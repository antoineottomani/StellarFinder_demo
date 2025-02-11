from pathlib import Path
import environ

# Global settings for production & development environments in demo version

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)

env = environ.Env()

SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG', default=False)
ALLOWED_HOSTS = []

DEMO_DATA_PATH = BASE_DIR / "equipment/demo_data.json"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'users',
    'equipment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.demo_mode',

            ],
        },
    },
]

WSGI_APPLICATION = 'stellarfinder.wsgi.application'

AUTH_PASSWORD_VALIDATORS = []

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'stellarfinder.urls'


LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]
STATIC_URL = '/static/'

# Media files (Uploaded files)
MEDIA_URL = '/media/'
# MEDIA_ROOT = [BASE_DIR / 'media']

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'users.CustomUser'

# URL to redirect after connexion success
LOGIN_REDIRECT_URL = 'mon-compte'
LOGIN_URL = 'connexion'
