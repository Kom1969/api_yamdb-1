from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime, timedelta
import jwt


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор')
]


class User(AbstractUser):
    email = models.EmailField(db_index=True, unique=True)
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Биография (о себе)',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        help_text='Роль пользователя с правами доступа',
        max_length=settings.USER_ROLE_MAX_LENGTH,
        choices=ROLES,
        default=USER,
    )

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
