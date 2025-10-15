    #!/bin/sh
    set -e
    export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-autorizaciones.settings}
    export PORT=${PORT:-8000}
    python -m django migrate --noinput
    python -m django collectstatic --noinput
    if [ -n "$DJANGO_SUPERUSER_NAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python - <<'PY'
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','autorizaciones.settings')
django.setup()
from django.contrib.auth.models import User
u, _ = User.objects.get_or_create(username=os.environ['DJANGO_SUPERUSER_NAME'], defaults={'email': os.environ['DJANGO_SUPERUSER_EMAIL']})
u.is_staff = True; u.is_superuser = True; u.set_password(os.environ['DJANGO_SUPERUSER_PASSWORD']); u.save()
print("Superuser ready:", u.username)
PY
    fi
    exec gunicorn autorizaciones.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
