# from django.contrib.auth import get_user_model
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(blank=True)
    rating = models.IntegerField()  # ограничения от 0 до 10?
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        default=0,
        on_delete=models.SET_DEFAULT,
        related_name='genres')
    category = models.ForeignKey(
        Genre,
        default=0,
        on_delete=models.SET_DEFAULT,
        related_name='categories')

    def __str__(self):
        return self.name
