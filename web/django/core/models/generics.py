from django.db import models
from django_currentuser.db.models import CurrentUserField


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ModifiedByMixin(models.Model):
    created_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_created_by",
        related_query_name="%(app_label)s_%(class)s_created_by",
    )
    updated_by = CurrentUserField(
        on_update=True,
        related_name="%(app_label)s_%(class)s_updated_by",
        related_query_name="%(app_label)s_%(class)s_updated_by",
    )

    class Meta:
        abstract = True
