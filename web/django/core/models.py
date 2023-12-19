from typing import Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models.functions import Lower


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    @staticmethod
    def create_user(
        email: str,
        name: str,
        password: Optional[str] = None,
    ) -> "User":
        if not email:
            raise ValueError("Users must have an email address")

        if not name:
            raise ValueError("Users must have a name")

        user: User = User.objects.create(
            email=UserManager.normalize_email(email),
            name=name,
        )

        if password is not None:
            user.set_password(password)

        return user

    @staticmethod
    def create_superuser(**kwargs) -> "User":
        user: User = UserManager.create_user(**kwargs)
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user


class User(TimestampMixin, PermissionsMixin, AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ("name",)

    email = models.EmailField("email address", max_length=255, unique=True)
    name = models.CharField(max_length=40)
    is_active = models.BooleanField("enabled user", db_default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="user_email_unique",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def get_full_name(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        return self.name

    def is_staff(self) -> bool:
        return self.is_superuser
