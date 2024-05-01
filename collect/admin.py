from django.contrib import admin

from .models import Collect, Event, Payment


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Интерфейс управления тегами."""

    list_display = (
        'id',
        'title',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'title',
    )
    list_display_links = ('title',)
    ordering = ('title',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Интерфейс управления платяжами."""

    list_display = (
        'collect',
        'user',
        'amount',
        'created_at',
    )
    search_fields = ('user__username',)
    list_filter = (
        'user__username',
        'collect__title',
    )
    list_display_links = ('user',)
    ordering = ('user',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    """Интерфейс управления сборами."""

    list_display = (
        'author',
        'title',
        'display_event',
        'text',
        'target_amount',
        'current_amount',
        'patrician_count',
        'cover',
        'endtime',
        'created_at',
    )
    exclude = ('list_payment',)
    search_fields = (
        'author__username',
        'collect__title',
    )
    list_filter = (
        'author__username',
    )
    list_display_links = ('author',)
    ordering = ('-created_at',)

    @admin.display(description='События')
    def display_event(self, obj):
        """Добавляет события в разделе сбора."""
        return ', '.join(
            event.title for event in obj.event.all()
        )
