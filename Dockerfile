FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev dos2unix \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Whitenoise / static
ENV DJANGO_SETTINGS_MODULE=autorizaciones.settings

# Entrypoint ejecutable (si usas el archivo de abajo)
RUN dos2unix scripts/entrypoint.sh && chmod +x scripts/entrypoint.sh

# Corre como usuario no-root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["scripts/entrypoint.sh"]
