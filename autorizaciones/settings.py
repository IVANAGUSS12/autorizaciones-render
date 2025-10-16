import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables del entorno (.env)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------
# CONFIGURACIÓN BÁSICA DJANGO
# ---------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = [
    ".ondigitalocean.app",
    "localhost",
    "127.0.0.1"
]

# ---------------------------------------------------------------------
# APLICACIONES
# ---------------------------------------------------------------------
INSTALLED_APPS = [
    # Django apps básicas
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros
    "rest_framework",
    "corsheaders",
    "storages",

    # App principal
    "core",
]

# ---------------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "autorizaciones.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "autorizaciones.wsgi.application"

# ---------------------------------------------------------------------
# BASE DE DATOS
# ---------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "autorizaciones"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# ---------------------------------------------------------------------
# CONTRASEÑAS / AUTENTICACIÓN
# ---------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------
# INTERNACIONALIZACIÓN
# ---------------------------------------------------------------------
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------
# ARCHIVOS ESTÁTICOS Y MEDIA
# ---------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ---------------------------------------------------------------------
# DIGITALOCEAN SPACES - CONFIGURACIÓN DE ARCHIVOS
# ---------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("SPACES_NAME")
AWS_S3_REGION_NAME = os.getenv("SPACES_REGION", "sfo3")
AWS_S3_ENDPOINT_URL = os.getenv("SPACES_ENDPOINT", "https://sfo3.digitaloceanspaces.com")
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", f"{AWS_STORAGE_BUCKET_NAME}.sfo3.digitaloceanspaces.com")

MEDIA_URL = os.getenv("MEDIA_URL", f"https://{AWS_S3_CUSTOM_DOMAIN}/")
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------------
# REST FRAMEWORK
# ---------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}

# ---------------------------------------------------------------------
# CORS (para permitir formularios externos)
# ---------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "https://autorizaciones-954773928377.southamerica-east1.run.app",
    "https://seahorse-app-c5449.ondigitalocean.app",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    "https://autorizaciones-954773928377.southamerica-east1.run.app",
    "https://seahorse-app-c5449.ondigitalocean.app",
]

# ---------------------------------------------------------------------
# SEGURIDAD
# ---------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


