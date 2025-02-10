#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def main():
    """Run administrative tasks."""

    # Load env variables
    env = environ.Env()
    environ.Env.read_env(env_file=str(
        BASE_DIR / "stellarfinder/.env"))

    # Set DJANGO_SETTINGS_MODULE based on the DJANGO_ENV environment variable
    env_setting = env('DJANGO_ENV', default='development')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          f'stellarfinder.settings.{env_setting}')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
