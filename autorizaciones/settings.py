import os
from pathlib import Path
import dj_database_url

# -----------------------------------------------------
# Paths / base
# -----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------
# Core / security
# -----------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-secret-key")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes", "on")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get(
        "ALLOWED_HOSTS",
        ".ondigitalocean.app,localhost,127.0.0.1"
    ).split(",")
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "https://*.ondigitalocean.app"
    ).split(",")
    if o.strip()
]

# -----------------------------------------------------
# Apps
# -----------------------------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd
    "rest_framework",
    "corsheaders",

    # Local
    "core",
]

# -----------------------------------------------------
# Middleware
# -----------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------------------------------
# URLs / WSGI
# -----------------------------------------------------
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

# -----------------------------------------------------
# Database (dj-database-url)
# -----------------------------------------------------
DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL", "postgres://user:pass@localhost:5432/dbname"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# -----------------------------------------------------
# Auth
# -----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------
# i18n / tz
# -----------------------------------------------------
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------
# Static
# -----------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
WHITENOISE_MAX_AGE = 60 * 60 * 24 * 30  # 30 días

# -----------------------------------------------------
# Storages (STATIC + MEDIA)
# - Local: FileSystem para MEDIA
# - Producción: DigitalOcean Spaces (S3) para MEDIA
# -----------------------------------------------------
def _env_bool(name: str, default: bool = False) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.lower() in ("1", "true", "yes", "on")

USE_SPACES = _env_bool("USE_SPACES", not DEBUG)

if USE_SPACES:
    # django-storages
    INSTALLED_APPS += ["storages"]

    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

    SPACES_NAME = os.environ["SPACES_NAME"]                 # bucket
    SPACES_REGION = os.environ.get("SPACES_REGION", "sfo3") # región
    SPACES_ENDPOINT = os.environ.get(
        "SPACES_ENDPOINT",
        f"https://{SPACES_REGION}.digitaloceanspaces.com",
    )

    AWS_S3_ENDPOINT_URL = SPACES_ENDPOINT
    AWS_S3_REGION_NAME = SPACES_REGION
    AWS_STORAGE_BUCKET_NAME = SPACES_NAME
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

    AWS_S3_CUSTOM_DOMAIN = os.environ.get(
        "AWS_S3_CUSTOM_DOMAIN",
        f"{SPACES_NAME}.{SPACES_REGION}.digitaloceanspaces.com",
    )

    STORAGES = {
        # Archivos de usuario -> Space
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        # Archivos estáticos -> whitenoise (ya empaquetados en la imagen)
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    # Las URLs de media serán absolutas al Space
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

else:
    # Desarrollo/local: MEDIA a disco
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    }

# -----------------------------------------------------
# Seguridad en prod
# -----------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
X_FRAME_OPTIONS = "DENY"
REFERRER_POLICY = "same-origin"

# -----------------------------------------------------
# DRF / CORS
# -----------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}

CORS_ALLOWED_ORIGINS = []   # podés poner dominios explícitos si querés
CORS_ALLOW_CREDENTIALS = True

# -----------------------------------------------------
# Login / Logout
# -----------------------------------------------------
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/panel/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

