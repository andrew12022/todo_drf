import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидатор проверки имени пользователя."""
    if value.lower() == 'me':
        raise ValidationError(
            'Ошибка! '
            'Использовать "me" в качестве имени пользователя запрещено'
        )
    if not re.fullmatch(r"^[\w.@+-]+\Z", value):
        raise ValidationError(
            'Ошибка! '
            'Недопустимые символы в имени пользователя. '
            'Можно использовать только буквы, цифры и символы @/./+/-/_'
        )
