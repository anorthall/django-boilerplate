import os

from django.core.asgi import get_asgi_application

env_kind = os.environ["ENV_KIND"]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.django.settings.{env_kind}")
application = get_asgi_application()
