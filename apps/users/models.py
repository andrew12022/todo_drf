from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.validators import validate_username
from config import constants


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_EMAIL,
        unique=True,
        verbose_name='Адрес электронной почты',
        help_text=(
            'Укажите действующий email (максимум 254 символа). '
            'Будет использоваться для входа в систему.'
        ),
        error_messages={
            'unique': 'Email уже занят',
        },
    )
    username = models.CharField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_USERNAME,
        unique=True,
        validators=[validate_username],
        verbose_name='Логин',
        help_text=(
            'Укажите уникальный логин (максимум 30 символов). '
            'Допустимы только буквы, цифры и символы @/./+/-/_.'
        ),
        error_messages={
            'unique': 'Логин уже занят',
        },
    )
    first_name = models.CharField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_NAME,
        blank=True,
        verbose_name='Имя',
        help_text='Укажите ваше имя (необязательно, максимум 50 символов)',
    )
    last_name = models.CharField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_NAME,
        blank=True,
        verbose_name='Фамилия',
        help_text=(
            'Укажите вашу фамилию (необязательно, максимум 50 символов)'
        ),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
    ]

    class Meta:
        ordering = ['-id']
        verbose_name = 'объект "Пользователь"'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
