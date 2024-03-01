import os

from celery import Celery

env_kind = os.environ["ENV_KIND"]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.django.settings.{env_kind}")

app = Celery("aicore")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
