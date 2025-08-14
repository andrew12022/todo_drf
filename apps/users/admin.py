from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from apps.users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Административная панель для управления пользователями."""

    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
    )
    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name',
    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
    )
    readonly_fields = (
        'last_login',
        'date_joined',
    )
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            ),
        }),
        ('Персональная информация', {
            'fields': (
                'first_name',
                'last_name',
                'username',
            ),
        }),
        ('Права доступа', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ('Важные даты', {
            'fields': (
                'last_login',
                'date_joined',
            ),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'first_name',
                'last_name',
                'password1',
                'password2',
            ),
        }),
    )


admin.site.unregister(Group)
