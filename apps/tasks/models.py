from django.contrib.auth.models import User
from django.core.validators import validate_slug
from django.db import models

from apps.tasks.validators import validate_deadline
from config import constants


class BaseModel(models.Model):
    """Абстрактная базовая модель для всех сущностей."""
    title = models.CharField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_TITLE_AND_SLUG,
        db_index=True,
        verbose_name='Название',
        help_text='Укажите название (максимум 150 символов)',
    )
    slug = models.SlugField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_TITLE_AND_SLUG,
        unique=False,
        validators=[validate_slug],
        verbose_name='URL-идентификатор',
        help_text=(
            'Укажите уникальный идентификатор URL (только латинские буквы, '
            'цифры, дефисы и подчёркивания)'
        ),
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_owned',
        verbose_name='Владелец',
        help_text='Пользователь, которому принадлежит этот объект',
    )

    class Meta:
        abstract = True
        ordering = ['-id']


class Task(BaseModel):
    """Модель задачи."""

    class Priority(models.TextChoices):
        """Варианты приоритетов для задачи."""
        LOW = 'LW', 'Низкий'
        MEDIUM = 'MD', 'Средний'
        HIGH = 'HG', 'Высокий'

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Подробное описание задачи (необязательно)',
    )
    is_done = models.BooleanField(
        default=False,
        verbose_name='Выполнено',
        help_text='Отметьте, если задача выполнена',
    )
    deadline = models.DateField(
        blank=True,
        null=True,
        validators=[validate_deadline],
        verbose_name='Срок выполнения',
        help_text=(
            'Укажите дату выполнения в формате '
            'ГГГГ-ММ-ДД (необязательно)'
        ),
    )
    priority = models.CharField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_PRIORITY,
        choices=Priority.choices,
        default=Priority.LOW,
        db_index=True,
        verbose_name='Приоритет',
        help_text='Выберите приоритет выполнения задачи',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name='Дата обновления',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='tasks',
        blank=True,
        null=True,
        verbose_name='Категория',
        help_text='Выберите категорию для задачи (необязательно)',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='tasks',
        blank=True,
        verbose_name='Теги',
        help_text='Выберите теги для задачи (необязательно)',
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'объект "Задача"'
        verbose_name_plural = 'Задачи'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'owner'],
                name='task_unique_title_owner',
                violation_error_message='Название уже занято',
            ),
            models.UniqueConstraint(
                fields=['slug', 'owner'],
                name='task_unique_slug_owner',
                violation_error_message='Идентификатор URL уже занят',
            )
        ]

    def __str__(self):
        return f'{self.title} (владелец: {self.owner.username})'


class Category(BaseModel):
    """Модель категории."""

    class Meta(BaseModel.Meta):
        verbose_name = 'объект "Категория"'
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'owner'],
                name='category_unique_title_owner',
                violation_error_message='Название уже занято',
            ),
            models.UniqueConstraint(
                fields=['slug', 'owner'],
                name='category_unique_slug_owner',
                violation_error_message='Идентификатор URL уже занят',
            )
        ]

    def __str__(self):
        return self.title


class Tag(BaseModel):
    """Модель тега."""

    class Meta(BaseModel.Meta):
        verbose_name = 'объект "Тег"'
        verbose_name_plural = 'Теги'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'owner'],
                name='tag_unique_title_owner',
                violation_error_message='Название уже занято',
            ),
            models.UniqueConstraint(
                fields=['slug', 'owner'],
                name='tag_unique_slug_owner',
                violation_error_message='Идентификатор URL уже занят',
            )
        ]

    def __str__(self):
        return self.title
