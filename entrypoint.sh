#!/bin/bash
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --no-input
gunicorn --bind 0.0.0.0:8000 app.wsgi:application
