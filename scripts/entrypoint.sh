#!/usr/bin/env bash
set -e

echo "🚀 Migrando base de datos..."
python manage.py migrate --noinput

echo "📦 Colectando estáticos..."
python manage.py collectstatic --noinput

echo "🔥 Levantando gunicorn..."
exec gunicorn autorizaciones.wsgi:application --bind 0.0.0.0:8080 --workers 3 --timeout 120

