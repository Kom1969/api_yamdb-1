import csv

from django.db.utils import IntegrityError
from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
)
from users.models import User


TABLES_DICT = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv',
}


class Command(BaseCommand):
    help = 'Load csv data'

    def handle(self, *args, **kwargs):
        new_raws = 0
        old_raws = 0

        for model, base in TABLES_DICT.items():
            with open(
                    f'{settings.CSV_DIR}/{base}', 'r', encoding='utf-8') as f:

                reader = csv.DictReader(f)
                for data in reader:
                    try:
                        if model == Title:
                            data['category'] = Category.objects.all().filter(
                                id=data['category'])[0]
                        elif model in (Review, Comment):
                            data['author'] = User.objects.all().filter(
                                id=data['author'])[0]
                        model.objects.create(**data)
                        new_raws += 1
                    except IntegrityError:
                        old_raws += 1

        print(
            f'All data in your Data Base now!\n'
            f'New entry: {new_raws}\nOld entry: {old_raws}')
