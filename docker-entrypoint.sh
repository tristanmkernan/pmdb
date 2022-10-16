#!/bin/sh
set -e

# python manage.py collectstatic --no-input
python manage.py migrate

gunicorn --workers=2 --bind=0.0.0.0:8000 pmdb.wsgi