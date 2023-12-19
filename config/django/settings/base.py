import os
from pathlib import Path
from typing import Any

import dj_database_url
from django.core.exceptions import ImproperlyConfigured


def env(name, default=None, force_type: Any = str):
    setting = os.environ.get(name, default)
    if setting is None:
        raise ImproperlyConfigured(f"{name} environment variable is not set")

    try:
        return force_type(setting)
    except ValueError:
        raise ImproperlyConfigured(
            f"{name} environment variable is not a valid {force_type.__name__}"
        )


# BASE_DIR should point to where manage.py is
if base_dir := env("BASE_DIR", ""):
    BASE_DIR = Path(base_dir)
else:
    raise ImproperlyConfigured("BASE_DIR environment variable is not set")

# Date formats
DATETIME_FORMAT = "H:i Y-m-d"
DATE_FORMAT = "Y-m-d"
TIME_FORMAT = "H:i"

# Site root URL with protocol and without a trailing slash
SITE_ROOT = env("SITE_ROOT", "http://127.0.0.1:8000")

# Security keys/options
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", "http://127.0.0.1").split(" ")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS", "http://127.0.0.1").split(" ")

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication
LOGIN_URL = "core:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
AUTH_USER_MODEL = "core.User"

# Django apps
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "core.apps.CoreConfig",
    "crispy_forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.postgres",
]

# Django middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Django templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates/")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

# Django wsgi
WSGI_APPLICATION = "config.django.wsgi.application"

# Django root urlconf
ROOT_URLCONF = "config.django.urls"

# Database
DATABASES = {
    "default": dj_database_url.config(
        default="postgres://postgres:postgres@db:5432/postgres",
        conn_max_age=env("CONN_MAX_AGE", 30, int),
        conn_health_checks=True,
    )
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Static files, media files, and Amazon S3.
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", "")
AWS_S3_ACCESS_KEY_ID = env("AWS_S3_ACCESS_KEY_ID", "")
AWS_S3_SECRET_ACCESS_KEY = env("AWS_S3_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", "")
AWS_S3_SIGNATURE_VERSION = env("AWS_S3_SIGNATURE_VERSION", "s3v4")
AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL", "private")
AWS_PRESIGNED_EXPIRY = env("AWS_PRESIGNED_EXPIRY", 20, int)

STATIC_URL = "/static/"
STATIC_ROOT = os.environ.get("STATIC_ROOT", "/app/staticfiles")
STATICFILES_DIRS = [BASE_DIR / ".." / "static"]

MEDIA_STORAGE_LOCATION = env("MEDIA_LOCATION", "media")

if AWS_STORAGE_BUCKET_NAME:  # pragma: no cover
    MEDIA_URL = env("MEDIA_URL")
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "location": MEDIA_STORAGE_LOCATION,
            },
        },
    }
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.environ.get("MEDIA_ROOT", "/app/mediafiles")
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": MEDIA_STORAGE_LOCATION,
            },
        },
    }

STORAGES["staticfiles"] = {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}
