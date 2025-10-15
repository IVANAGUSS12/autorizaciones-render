FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# agrego dos2unix para convertir CRLF->LF
RUN apt-get update && apt-get install -y build-essential libpq-dev dos2unix && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copio el proyecto
COPY . .

ENV DJANGO_SETTINGS_MODULE=autorizaciones.settings

# convierto finales de línea y doy permisos de ejecución
RUN dos2unix scripts/entrypoint.sh && chmod +x scripts/entrypoint.sh

# creo usuario no-root y doy ownership
RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["scripts/entrypoint.sh"]
