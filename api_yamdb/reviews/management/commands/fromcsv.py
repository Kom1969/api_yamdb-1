import csv

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

        for model, base in TABLES_DICT.items():
            with open(
                    f'{settings.CSV_DIR}/{base}', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                models = []
                for data in reader:
                    ids = [m.id for m in model.objects.all()]
                    if model == Title:
                        data['category'] = Category.objects.get(
                            id=data['category'])
                    elif model in (Review, Comment):
                        data['author'] = User.objects.get(
                            id=data['author'])
                    ids = [m.id for m in model.objects.all()]
                    if int(data['id']) not in ids:
                        models.append(model(**data))
                        ids.append(int(data['id']))
                model.objects.bulk_create(models)
