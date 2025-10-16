# autorizaciones/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------- Básicos --------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-unsafe")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    "ALLOWED_HOSTS",
    ".ondigitalocean.app,localhost,127.0.0.1"
).split(",") if h.strip()]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [u.strip() for u in os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://*.ondigitalocean.app"
).split(",") if u.strip()]

# -------------------- Apps / Middleware --------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
    }
]

WSGI_APPLICATION = "autorizaciones.wsgi.application"

# -------------------- Base de datos --------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", ""),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}
if os.getenv("DATABASE_URL"):
    import dj_database_url
    DATABASES["default"] = dj_database_url.parse(
        os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )

# -------------------- Static / Media --------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

USE_S3 = os.getenv("USE_S3", "False").lower() == "true"

if USE_S3:
    INSTALLED_APPS.append("storages")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", os.getenv("SPACES_REGION", "sfo3"))
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", os.getenv("SPACES_NAME", ""))
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL", os.getenv("SPACES_ENDPOINT", "https://sfo3.digitaloceanspaces.com"))
    AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", "")  # p.ej. autorizaciones.sfo3.digitaloceanspaces.com
    AWS_DEFAULT_ACL = os.getenv("AWS_DEFAULT_ACL", "public-read")
    AWS_QUERYSTRING_AUTH = os.getenv("AWS_QUERYSTRING_AUTH", "False").lower() == "true"
    AWS_LOCATION = os.getenv("AWS_LOCATION", "media")

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
        if AWS_LOCATION:
            MEDIA_URL += f"{AWS_LOCATION}/"
    else:
        MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"
        if AWS_LOCATION:
            MEDIA_URL += f"{AWS_LOCATION}/"

    MEDIA_ROOT = ""
else:
    MEDIA_URL = os.getenv("MEDIA_URL", "/media/")
    MEDIA_ROOT = os.getenv("MEDIA_ROOT", str(BASE_DIR / "media"))

# -------------------- Tamaños de subida --------------------
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv("FILE_UPLOAD_MAX_MEMORY_SIZE", str(15 * 1024 * 1024)))
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv("DATA_UPLOAD_MAX_MEMORY_SIZE", str(25 * 1024 * 1024)))
FILE_UPLOAD_PERMISSIONS = 0o644

# -------------------- CORS --------------------
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv(
    "CORS_ALLOWED_ORIGINS", ""
).split(",") if o.strip()]
CORS_ALLOW_CREDENTIALS = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
