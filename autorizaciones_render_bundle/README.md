# Autorizaciones · Render Bundle
- Django + DRF + Postgres + Disco persistente
- Endurecido para producción

## Deploy en Render
1. Repo con este contenido.
2. Render -> Blueprint -> `render.yaml`.
3. Variables: `DJANGO_SECRET_KEY` (auto), `DEBUG=False`, `ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1`, `CSRF_TRUSTED_ORIGINS=https://*.onrender.com`.
4. (Opcional) `DJANGO_SUPERUSER_*` para crear admin en la primera subida.
5. Accedé a `/accounts/login/` y luego `/panel/`.

## API compatible con tus HTML:
- POST /v1/patients/
- POST /v1/attachments/
- GET/PATCH /v1/patients/<id>/
