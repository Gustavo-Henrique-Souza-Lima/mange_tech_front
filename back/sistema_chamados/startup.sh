#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn --bind=0.0.0.0:8000 sistema_chamados.wsgi