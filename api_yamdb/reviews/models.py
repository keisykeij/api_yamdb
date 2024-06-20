from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .vaidators import validate_year

from users.models import CustomUser


class Title(models.Model):
    name = models.CharField('Название', max_length=256, db_index=True)
    year = models.IntegerField('Год выпуска', validators=(validate_year,))
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField('Genre', verbose_name='Жанр',
                                   related_name='titles')
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название категории', max_length=50)
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=50)
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


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
