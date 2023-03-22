from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import username_validator


class User(AbstractUser):

    class Roles(models.Choices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    username = models.CharField(
        verbose_name='Юзернейм',
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
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
        choices=Roles.choices,
        default=Roles.USER,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    # Не могу допереть, как тут строки заменить
    # User.Roles.ADMIN не работает.
    @property
    def is_admin(self):
        return self.role == User.Roles.ADMIN._value_ or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.Roles.MODERATOR._value_
