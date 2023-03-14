# from django.contrib.auth import get_user_model
from django.db import models


class Genre(models.model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(blank=True)
    rating = models.IntegerField() # ограничения от 0 до 10?
    description = models.TextField() # text - т.к. нет ограничений на длину строки
    genre = models.ForeignKey(Genre, related_name='titles') # on_delete=models.CASCADE - не это, но что? 
    category = models.ForeignKey(Genre, related_name='titles') # on_delete=models.CASCADE - не это, но что? 

    def __str__(self):
        return self.name
