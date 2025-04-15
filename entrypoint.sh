#!/bin/sh

# Arrête le script si une commande échoue
set -e

echo "Collecting static files..."
python src/manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec gunicorn stellarfinder.wsgi:application --chdir src --bind 0.0.0.0:8000
