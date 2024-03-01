from django.conf import settings
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import User

admin.site.site_header = settings.ADMIN_TITLE
admin.site.site_title = settings.ADMIN_TITLE
admin.site.index_title = settings.ADMIN_TITLE


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("email", "name", "is_active", "last_login")
    list_filter = ("is_active", "created_at")
    search_fields = ("email", "name")
    readonly_fields = ("last_login", "created_at")
    fieldsets = (
        ("User information", {"fields": ("email", "name")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_superuser", "groups", "user_permissions")},
        ),
        ("Metadata", {"fields": ("last_login", "created_at")}),
    )
