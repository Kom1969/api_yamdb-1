import re

from django.conf import settings
from django.core.exceptions import ValidationError

from users.models import User


def username_validator(data):
    if data.lower() == 'me':
        raise ValidationError('Использование юзернейма "me" запрещено.')

    # Регулярки - зло.
    # ^[\w.@+-]+\z
    if not re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', data):
        raise ValidationError(
            'Вы не можете использовать спецсимволы в юзернейме.'
        )


def signup_validator(data):
    email = data['email']
    username = data['username']
    if (User.objects.filter(email=email).exists()
            and not User.objects.filter(username=username).exists()):
        raise ValidationError('Попробуйте указать другую электронную почту.')
    if (not User.objects.filter(email=email).exists()
            and User.objects.filter(username=username).exists()):
        raise ValidationError('Попробуйте указать другой юзернейм.')
    return data


def score_validator(data):
    score = data['score']
    if not settings.REVIEW_MIN_SCORE < score <= settings.REVIEW_MAX_SCORE:
        raise ValidationError(
            'Рейтинг произведения должен быть от 1 до 10.'
        )
    return data


def year_validator(data):
    year = data['year']
    if year >= settings.MAX_YEAR:
        raise ValidationError(
            'Год выпуска произведения должен быть меньше текущего.'
        )
    return data
