from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models


class ROLES(Enum):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'


class CustomUser(AbstractUser):
    email = models.EmailField('email', unique=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=9,
        choices=((role.value, role.name) for role in ROLES),
        default=ROLES.user.value
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='Unique auth data constraint'
            ),
        )
