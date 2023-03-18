import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, User, GenreTitle, Genre, Title, Review, Comment
from django.conf import settings
from django.db.utils import IntegrityError


class Command(BaseCommand):

    help = 'Add data to the database'

    def handle(self, *args, **kwargs):

        new_raws = 0
        old_raws = 0

        # Import Users
        with open(settings.CSV_DIR / 'users.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if row[0] != 'id':
                        User.objects.create(
                            id=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3],
                            bio=row[4],
                            first_name=row[5],
                            last_name=row[6])
                        new_raws += 1
                except IntegrityError:
                    old_raws += 1

        with open(settings.CSV_DIR / 'genre.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if row[0] != 'id':
                        Genre.objects.create(
                            id=row[0],
                            name=row[1],
                            slug=row[2])
                        new_raws += 1
                except IntegrityError as err:
                    old_raws += 1

        with open(settings.CSV_DIR / 'category.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if row[0] != 'id':
                        Category.objects.create(
                            id=row[0],
                            name=row[1],
                            slug=row[2])
                        new_raws += 1
                except IntegrityError as err:
                    old_raws += 1

        with open(settings.CSV_DIR / 'titles.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if row[0] != 'id':
                        category = Category.objects.all().filter(id=row[3])[0]
                        Title.objects.create(
                            id=row[0],
                            name=row[1],
                            year=row[2],
                            category=category)
                        new_raws += 1
                except IntegrityError as err:
                    old_raws += 1


        with open(settings.CSV_DIR / 'genre_title.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if row[0] != 'id':
                        GenreTitle.objects.create(
                            id=row[0],
                            title_id=row[1],
                            genre_id=row[2],)
                        new_raws += 1
                except IntegrityError as err:
                    old_raws += 1

        with open(settings.CSV_DIR / 'review.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if row[0] != 'id':
                        author = User.objects.all().filter(id=row[3])[0]
                        title = Title.objects.all().filter(id=row[1])[0]
                        Review.objects.create(
                            id=row[0],
                            title=title,
                            text=row[2],
                            author=author,
                            score=row[4],
                            pub_date=row[5])
                        new_raws += 1
                except IntegrityError:
                    old_raws += 1

        with open(settings.CSV_DIR / 'comments.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if row[0] != 'id':
                        author = User.objects.all().filter(id=row[3])[0]
                        review = Review.objects.all().filter(id=row[1])[0]
                        Comment.objects.create(
                            id=row[0],
                            review=review,
                            text=row[2],
                            author=author,
                            pub_date=row[4])
                        new_raws += 1
                except IntegrityError:
                    old_raws += 1
        
        print(f'All data in your Data Base now!\nNew entry: {new_raws}\nOld entry: {old_raws}')
