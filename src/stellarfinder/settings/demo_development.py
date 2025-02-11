from .settings import *

environ.Env.read_env(env_file=str(BASE_DIR / "stellarfinder/.env"))

INSTALLED_APPS += [
    'livereload',
    'debug_toolbar',
]

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

MIDDLEWARE += [
    'livereload.middleware.LiveReloadScript',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

# Configuration for database in development
DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE'),
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}
