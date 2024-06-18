from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


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


class ConfirmationCode(models.Model):
    confirmation_code = models.CharField(max_length=36)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code'
    )

    # TODO: Протестить будет ли обновляться код если
    #       его жестко передать при создании объекта
    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = get_random_string(length=36)
            super().save(*args, **kwargs)
