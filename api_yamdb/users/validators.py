import re

from django.core.exceptions import ValidationError


def username_validator(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Использование юзернейма "me" запрещено.',
        )

    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            'Вы не можете использовать спецсимволы в юзернейме.',
        )
    return value
