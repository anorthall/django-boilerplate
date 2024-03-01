import socket

from .base import *

DEBUG = False

# Security
SECURE_HSTS_SECONDS = env("SECURE_HSTS_SECONDS", 0, force_type=int)
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", default=False, force_type=int)
SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD", default=False, force_type=int)
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", default=False, force_type=int)
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", default=False, force_type=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=False,
    force_type=int,
)

# Only enable if required
if env("SECURE_PROXY_SSL_HEADER", default=False, force_type=int):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

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

# Add Docker host IP to ALLOWED_HOSTS for Dokku healthchecks
ALLOWED_HOSTS.append(socket.getaddrinfo(socket.gethostname(), "http")[0][4][0])
