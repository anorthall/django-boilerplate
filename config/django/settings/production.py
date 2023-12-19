from .base import *

DEBUG = False

# Security
SECURE_HSTS_SECONDS = env("SECURE_HSTS_SECONDS", 0, int)
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", False, int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env("SECURE_HSTS_INCLUDE_SUBDOMAINS", False, int)
SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD", False, int)
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", False, int)
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", False, int)

# Only enable if required
if env("SECURE_PROXY_SSL_HEADER", False, int):
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
