from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор')
]


class User(AbstractUser):
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
    email = models.EmailField(
        verbose_name='Электронная почта',
        help_text='Электронная почта',
        unique=True,
    )
    confirmation_code = models.CharField(
        max_length=32,
        blank=True,
    )

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

    def __str__(self):
        if self.username:
            return self.username
        return self.email
