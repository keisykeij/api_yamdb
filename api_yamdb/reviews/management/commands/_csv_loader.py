import csv

from users.models import CustomUser
from reviews.models import Genre, Category, Title, Review, Comment


class CSVLoader:
    """Абстрактный класс Загрузчика из CSV."""

    fields = None
    csv_filename = None
    object_class = None
    is_format_data = False

    def get_filename(self):
        """Функция формирования пути."""
        return f'static/data/{self.csv_filename}'

    def _get_format_data(self):
        """Функция первоначального преобразования данных."""
        with open(self.get_filename(), 'r') as file:
            reader = csv.reader(file.readlines())

            lines = list(reader)
            self.fields = lines.pop(0)

            all_data = (
                {key: value for key, value in zip(self.fields, line)}
                for line in lines
            )

            return all_data

    def fromat_data(self, data):
        """Функция дополнительного форматирования."""

        raise NotImplementedError

    def load_to_db(self):
        """Функция непосредственной загрузки данных в БД."""
        all_data = self._get_format_data()

        if self.is_format_data:
            all_data = self.fromat_data(all_data)

        objects = (self.object_class(**data) for data in all_data)

        self.object_class.objects.bulk_create(
            objects
        )

        return True


class UserCSVLoader(CSVLoader):
    """Загрузчик для модели Пользователя."""

    csv_filename = 'users.csv'
    object_class = CustomUser


class GenreCSVLoader(CSVLoader):
    """Загрузчик для модели Жанра."""
    csv_filename = 'genre.csv'
    object_class = Genre


class CategoryCSVLoader(CSVLoader):
    """"Загрузчик для модели Категории."""

    csv_filename = 'category.csv'
    object_class = Category


class TitleCSVLoader(CSVLoader):
    """Загрузчик для модели Произведения."""

    csv_filename = 'titles.csv'
    object_class = Title
    is_format_data = True

    def fromat_data(self, data):
        data = list(data)

        categories = {
            category.id: category for category in Category.objects.all()
        }

        for obj in data:
            category_id = obj.get('category')
            category = categories.get(int(category_id))
            obj['category'] = category

        return data


class TitleGenreCSVLoader(CSVLoader):
    """Загрузчик для модели многие-ко-многим"""
    """для моделей Произведения и Жанра."""

    csv_filename = 'genre_title.csv'
    object_class = Title.genre.through


class ReviewCSVLoader(CSVLoader):
    """Загрузчик для модели Отзыва."""

    csv_filename = 'review.csv'
    object_class = Review
    is_format_data = True

    def fromat_data(self, data):
        data = list(data)

        authors = {
            author.id: author for author in CustomUser.objects.all()
        }

        for obj in data:
            author_id = obj.get('author')
            author = authors.get(int(author_id))
            obj['author'] = author

        return data


class CommentCSVLoader(ReviewCSVLoader):
    """Загрузчик для модели Комментария."""

    csv_filename = 'comments.csv'
    object_class = Comment
