#!/bin/sh
set -e

echo "🚀 Migrando base de datos..."
python manage.py migrate --noinput

echo "📦 Colectando estáticos..."
python manage.py collectstatic --noinput

echo "🟢 Iniciando Gunicorn..."
exec gunicorn autorizaciones.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 3 --timeout 120
