from django.db import models


class Title(models.Model):
    name = models.CharField('Название', max_length=256, db_index=True)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', max_length=256,
                                   null=True, blank=True)
    genre = models.ManyToManyField('Genre', verbose_name='Жанр',
                                   related_name='titles', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True, blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название категории', max_length=50)
    slug = models.SlugField('Слаг категории', max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=50)
    slug = models.SlugField('Слаг жанра', max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name
