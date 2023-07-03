from .base import *

# Debug should always be off in production
DEBUG = False

# Security
SECURE_HSTS_SECONDS = env("SECURE_HSTS_SECONDS", 0, int)
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", False, bool)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env("SECURE_HSTS_INCLUDE_SUBDOMAINS", False, bool)
SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD", False, bool)
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", False, bool)
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", False, bool)
if env("SECURE_PROXY_SSL_HEADER", False, bool):  # Only enable if required
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Logging
DEFAULT_LOG_LEVEL = "WARNING"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": env("DJANGO_LOG_LEVEL", DEFAULT_LOG_LEVEL),
            "class": "logging.FileHandler",
            "filename": "/opt/app/logs/django/django.log",
        },
        "console": {
            "level": env("DJANGO_LOG_LEVEL", DEFAULT_LOG_LEVEL),
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": env("DJANGO_LOG_LEVEL", DEFAULT_LOG_LEVEL),
            "propagate": True,
        },
    },
}

# Sentry integration
if env("SENTRY_KEY", ""):  # pragma: no cover
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env("SENTRY_KEY"),
        integrations=[
            DjangoIntegration(),
        ],
        traces_sample_rate=0.2,
        send_default_pii=True,
    )
