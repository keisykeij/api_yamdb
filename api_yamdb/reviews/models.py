from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User  # type: ignore


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(validators=[
                                MinValueValidator(1),
                                MaxValueValidator(10),
                                ],)
    pub_date = models.DateTimeField(auto_now_add=True)
