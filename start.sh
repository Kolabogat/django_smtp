#!/bin/sh

python manage.py collectstatic
python manage.py makemigrations --no-input
python manage.py migrate --no-input
DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL
python manage.py runserver 0.0.0.0:8000
