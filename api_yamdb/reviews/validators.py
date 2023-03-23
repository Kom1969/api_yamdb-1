from django.conf import settings
from django.core.exceptions import ValidationError


def year_validator(data):
    if data >= settings.MAX_YEAR:
        raise ValidationError(
            'Год выпуска произведения должен быть меньше текущего.',
        )
    return data
