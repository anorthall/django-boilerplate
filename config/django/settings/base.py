import os
from pathlib import Path
from typing import Any

from django.contrib.messages import constants as messages
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
base_dir = env("BASE_DIR", "")
if base_dir:
    BASE_DIR = Path(base_dir)
else:
    raise ImproperlyConfigured("BASE_DIR environment variable is not set")


# Debug
DEBUG = env("DEBUG", False, bool)

# Site root URL with protocol and without a trailing slash
SITE_ROOT = env("SITE_ROOT", "http://127.0.0.1:8000")

# Security keys/options
# WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", "http://127.0.0.1").split(" ")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS", "http://127.0.0.1").split(" ")

# Email settings
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "")
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
MAILER_EMAIL_BACKEND = env(
    "MAILER_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
MAILER_EMPTY_QUEUE_SLEEP = env("MAILER_EMPTY_QUEUE_SLEEP", 30, int)
EMAIL_HOST = env("EMAIL_HOST", "")
EMAIL_PORT = env("EMAIL_PORT", 0, int)
EMAIL_USE_SSL = env("EMAIL_USE_SSL", False, bool)
EMAIL_USE_TLS = env("EMAIL_USE_TLS", False, bool)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

# Application definitions
INSTALLED_APPS = [
    "core.apps.CoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap5",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.LastSeenMiddleware",
]

# URLs
ROOT_URLCONF = "config.django.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

# WSGI configuration
WSGI_APPLICATION = "config.django.wsgi.application"

# ASGI configuration
ASGI_APPLICATION = "config.django.asgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": env("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": env("SQL_USER", "user"),
        "PASSWORD": env("SQL_PASSWORD", "password"),
        "HOST": env("SQL_HOST", "localhost"),
        "PORT": env("SQL_PORT", "5432", int),
        "ATOMIC_REQUESTS": env("SQL_ATOMIC_REQUESTS", True, bool),
    }
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication
AUTH_USER_MODEL = "core.AppUser"
LOGIN_URL = "core:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
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

# Bootstrap 5 message CSS classes
MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Rich test runner
TEST_RUNNER = "django_rich.test.RichRunner"

# Storages
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Media files
MEDIA_ROOT = env("MEDIA_ROOT", "/opt/app/mediafiles/")
MEDIA_URL = env("MEDIA_URL", "/media/")

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = env("STATIC_ROOT", "/opt/app/staticfiles")
STATIC_URL = env("STATIC_URL", "/static/")
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
