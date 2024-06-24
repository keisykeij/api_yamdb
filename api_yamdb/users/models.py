from enum import Enum

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class ROLES(Enum):
    """Перечисление для разграничения прав доступа пользователей."""
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'


class CustomUserManager(BaseUserManager):
    """Собственная модель менеджера для создания суперпользователя """
    """сразу с правами админа приложения."""

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, email, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        extra_fields['role'] = ROLES.admin.value

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Собственная модель пользователя для реализации ТЗ."""

    email = models.EmailField('email', max_length=254, unique=True)
    bio = models.TextField(default="", blank=True, null=True)
    role = models.CharField(
        max_length=9,
        choices=((role.value, role.name) for role in ROLES),
        default=ROLES.user.value
    )

    objects = CustomUserManager()

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='Unique auth data constraint'
            ),
        )
        ordering = ('id',)

    def __str__(self) -> str:
        return f'{self.username}: {self.role}'
