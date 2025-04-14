from django import forms
from django.contrib import admin

from apps.tasks.models import Category, Tag, Task


class TaskAdminForm(forms.ModelForm):
    """Кастомная форма для административной панели задач."""

    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'owner' in self.initial:
            self.fields['category'].queryset = Category.objects.filter(
                owner=self.initial['owner']
            )
            self.fields['tags'].queryset = Tag.objects.filter(
                owner=self.initial['owner']
            )

    def clean(self):
        cleaned_data = super().clean()
        owner = cleaned_data.get('owner')
        category = cleaned_data.get('category')
        tags = cleaned_data.get('tags', [])

        if category and category.owner != owner:
            raise forms.ValidationError(
                f'Категория "{category.title}" '
                'принадлежит другому пользователю!'
            )

        for tag in tags:
            if tag.owner != owner:
                raise forms.ValidationError(
                    f'Тег "{tag.title}" принадлежит другому пользователю!'
                )

        return cleaned_data


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Административная панель для управления задачами."""
    form = TaskAdminForm
    list_display = (
        'title',
        'owner',
        'is_done',
        'deadline',
        'priority',
        'category',
        'display_tags',
        'created_at',
        'updated_at',
    )
    list_editable = (
        'is_done',
        'priority',
    )
    search_fields = (
        'title',
        'description',
        'owner__username',
    )
    list_filter = (
        'is_done',
        'priority',
        'category',
        'tags',
        'owner',
        'created_at',
        'updated_at',
    )
    raw_id_fields = (
        'owner',
        'category',
    )
    filter_horizontal = (
        'tags',
    )
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'owner')
        }),
        ('Статус', {
            'fields': ('is_done', 'priority', 'deadline'),
        }),
        ('Классификация', {
            'fields': ('category', 'tags'),
        }),
    )

    @admin.display(description='Теги')
    def display_tags(self, obj):
        return ', '.join([tag.title for tag in obj.tags.all()])


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административная панель для управления категориями."""
    list_display = (
        'title',
        'slug',
        'owner',
    )
    search_fields = (
        'title',
        'owner__username',
    )
    list_filter = (
        'owner',
    )
    raw_id_fields = (
        'owner',
    )
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'owner')
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Административная панель для управления тегами."""
    list_display = (
        'title',
        'slug',
        'owner',
    )
    search_fields = (
        'title',
        'owner__username',
    )
    list_filter = (
        'owner',
    )
    raw_id_fields = (
        'owner',
    )
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'owner')
        }),
    )
