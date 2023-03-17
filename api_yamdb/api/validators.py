import re
from django.conf import settings
from django.core.exceptions import ValidationError

from users.models import User


def username_validator(data):
    if data.lower() == 'me':
        raise ValidationError('Использование юзернейма "me" запрещено.')

    if not re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', data):
        raise ValidationError('Вы можете использовать только буквы, цифры и нижнее подчёркивание.')


def signup_validator(data):
    email = data['email']
    username = data['username']
    if User.objects.filter(email=email).exists() and not User.objects.filter(username=username).exists():
        raise ValidationError('s')
    if not User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists():
        raise ValidationError('s')
    return data


def score_validator(data):
    score = data['score']
    if score < settings.REVIEW_MIN_VALUE or score > settings.REVIEW_MAX_VALUE:
        raise ValidationError(
            'Рейтинг произведения должен быть от 1 до 10')
    return data
