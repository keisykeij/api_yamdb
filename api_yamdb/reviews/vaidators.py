from django.utils import timezone
from rest_framework.exceptions import ValidationError


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше текущего {now}'
        )
