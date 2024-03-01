import socket

from .base import *

DEBUG = True
TEST_RUNNER = "django_rich.test.RichRunner"

INSTALLED_APPS += [
    "debug_toolbar",
    "django_browser_reload",
    "django_extensions",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# Find local IPs for debug toolbar
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
    "127.0.0.1",
    "10.0.2.2",
    "192.168.65.1",
]

# django-silk
# INSTALLED_APPS += ["silk"]
# MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")
# SILKY_PYTHON_PROFILER = True
# SILKY_PYTHON_PROFILER_BINARY = True
