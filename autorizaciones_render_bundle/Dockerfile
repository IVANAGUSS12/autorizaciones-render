FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=autorizaciones.settings
RUN chmod +x scripts/entrypoint.sh
RUN useradd -m appuser && chown -R appuser /app
USER appuser
CMD ["scripts/entrypoint.sh"]
