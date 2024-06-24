from typing import Any
import csv

from django.core.management.base import BaseCommand, CommandError
from users.models import CustomUser
from reviews.models import Genre, Category, Title


class CSVLoader:
    fields = None
    csv_filename = None
    object_class = None

    def load_to_db(self):
        with open(self.csv_filename, 'r') as file:
            reader = csv.reader(file.readlines())

            lines = list(reader)
            lines.pop(0)

            all_data = (
                {key: value for key, value in zip(self.fields, line)}
                for line in lines
            )

            objects = (self.object_class(**data) for data in all_data)

            self.object_class.objects.bulk_create(
                objects
            )


class UserCSVLoader(CSVLoader):
    fields = ['id', 'username', 'email', 'role']
    csv_filename = 'static/data/users.csv'
    object_class = CustomUser


class GenreCSVLoader(CSVLoader):
    fields = ['id', 'name', 'slug']
    csv_filename = 'static/data/genre.csv'
    object_class = Genre


class CategoryCVSLoader(CSVLoader):
    fields = ['id', 'name', 'slug']
    csv_filename = 'static/data/category.csv'
    object_class = Category


class TitleCSVLoader(CSVLoader):
    fields = ['id', 'name', 'year', 'category']
    csv_filename = 'static/data/titles.csv'
    object_class = Title


class Command(BaseCommand):
    help = 'Load data from csv-file to DB.'

    def handle(self, *args: Any, **options: Any) -> str | None:
        loader = TitleCSVLoader()
        loader.load_to_db()
