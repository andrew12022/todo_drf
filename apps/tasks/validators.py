from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_deadline(value):
    """Валидатор проверки дедлайна задачи."""

    today = timezone.now().date()
    if value < today:
        raise ValidationError(
            'Ошибка! '
            f'Нельзя установить дату {value}, т.к. уже {today}'
        )
