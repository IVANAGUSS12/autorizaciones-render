#!/usr/bin/env bash
set -e

echo "🚀 Collecting static..."
python manage.py collectstatic --noinput

echo "🚀 Applying migrations..."
python manage.py migrate --noinput

echo "🚀 Starting gunicorn..."
exec gunicorn autorizaciones.wsgi:application \
  --bind 0.0.0.0:8080 \
  --workers 3 \
  --timeout 120

