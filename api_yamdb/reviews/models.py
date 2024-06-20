from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import CustomUser


class Review(models.Model):
    title = models.ForeignKey(  # TODO нужно проверить
        Title, verbose_name='Название произведения',
        on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        CustomUser, verbose_name='Username пользователя',
        on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField('Оценка', validators=[
                                MinValueValidator(1), MaxValueValidator(10),],)
    pub_date = models.DateTimeField('Дата публикации отзыва',
                                    auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text
