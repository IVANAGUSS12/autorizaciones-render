# Imagen base ligera con Python 3.11
FROM python:3.11-slim

# --- Configuración básica de Python ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# --- Paquetes del SO necesarios ---
# build-essential   -> compilar dependencias de Python
# libpq-dev         -> soporte PostgreSQL (psycopg2)
# libjpeg/zlib      -> soporte de imágenes para Pillow (JPG/PNG)
# dos2unix          -> convertir CRLF a LF en scripts (Windows -> Linux)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      libjpeg62-turbo-dev \
      zlib1g-dev \
      dos2unix \
 && rm -rf /var/lib/apt/lists/*

# --- Directorio de trabajo ---
WORKDIR /app

# --- Dependencias de Python ---
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# --- Código de la app ---
COPY . .

# Ajustá si tu settings module es otro
ENV DJANGO_SETTINGS_MODULE=autorizaciones.settings

# --- Entrypoint: normaliza fin de línea y hace ejecutable ---
RUN dos2unix scripts/entrypoint.sh && chmod +x scripts/entrypoint.sh

# --- Carpeta de media (para uploads) y permisos ---
# /data/media es donde tu Django guardará archivos (MEDIA_ROOT)
RUN mkdir -p /data/media

# --- Usuario no-root ---
RUN useradd -m appuser \
 && chown -R appuser:appuser /app \
 && chown -R appuser:appuser /data
USER appuser

# Puerto típico de gunicorn (si lo exponés)
EXPOSE 8080

# --- Arranque de la app ---
CMD ["scripts/entrypoint.sh"]

