import re
from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Использование юзернейма "me" запрещено.')

    if not re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value):
        raise ValidationError('Атата.')
