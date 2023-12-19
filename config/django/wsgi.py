import os

from django.core.wsgi import get_wsgi_application

env_kind = os.environ["ENV_KIND"]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.django.settings.{env_kind}")
application = get_wsgi_application()
