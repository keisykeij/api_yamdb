from typing import Any

from django.core.management.base import BaseCommand, CommandError

from reviews.management.commands._csv_loader import (
    UserCSVLoader, GenreCSVLoader, CategoryCSVLoader, TitleCSVLoader,
    TitleGenreCSVLoader, ReviewCSVLoader, CommentCSVLoader
)


class Command(BaseCommand):
    help = 'Load data from csv-file to DB.'

    def handle(self, *args: Any, **options: Any):
        models = [
            UserCSVLoader, GenreCSVLoader, CategoryCSVLoader, TitleCSVLoader,
            TitleGenreCSVLoader, ReviewCSVLoader, CommentCSVLoader
        ]
        for Loader in models:
            loader = Loader()
            try:
                loader.load_to_db()
                self.stdout.write(
                    f'Applying {loader.csv_filename.capitalize()} model ... OK'
                )
            except Exception as ex:
                raise CommandError(ex)
        self.stdout.write('All models are successfull loaded.')
