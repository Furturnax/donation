from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User

admin.site.empty_value_display = 'Не задано'

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Интерфейс управления пользователями."""

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name')})
    )
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'first_name',
        'email',
    )
    list_display_links = ('username',)
    ordering = ('last_name', 'first_name')
