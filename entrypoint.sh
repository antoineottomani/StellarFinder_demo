#!/bin/sh

# Arrête le script si une commande échoue
set -e


# Vérifie que DJANGO_SECRET_KEY est défini
if [ -z "$DJANGO_SECRET_KEY" ]; then
    echo "Error: DJANGO_SECRET_KEY is not set."
    exit 1
fi

echo "Django secret key is set."

echo "Collecting static files..."
python src/manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec gunicorn stellarfinder.wsgi:application --chdir src --bind 0.0.0.0:8000
