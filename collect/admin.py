from decimal import Decimal

from django.contrib import admin
from django.db.models import Count, Sum, Prefetch
from django.utils.safestring import mark_safe

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
    list_display_links = ('title',)
    ordering = ('title',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Интерфейс управления платяжами."""

    list_display = (
        'user',
        'amount',
        'created_at',
        'display_collect',
    )
    search_fields = (
        'user__username',
        'collect__title',
    )
    list_filter = (
        'user__username',
        'collect__title',
    )
    list_display_links = ('display_collect',)
    ordering = ('-created_at',)

    @admin.display(description='Название сбора')
    def display_collect(self, obj):
        return obj.collect.title


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    """Интерфейс управления сборами."""

    list_display = (
        'author',
        'title',
        'display_event',
        'text',
        'target_amount',
        'display_current_amount',
        'display_patrician_count',
        'cover_tag',
        'endtime',
        'created_at',
    )
    search_fields = (
        'author__username',
        'title',
    )
    list_filter = (
        'created_at',
        'endtime',
    )
    list_display_links = ('author',)
    ordering = ('-created_at',)
    readonly_fields = ('cover_tag',)

    def get_queryset(self, request):
        """Получаем кверисет Collect."""

        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_amount=Sum('payments__amount'),
            uniq_patrician=Count('payments__user', distinct=True),
        )
        queryset = queryset.prefetch_related(
            Prefetch(
                'event', queryset=Event.objects.all()
            ),
        )
        return queryset

    @admin.display(description='Событие')
    def display_event(self, obj):
        """Добавляет события в разделе сбора."""
        return ', '.join(
            event.title for event in obj.event.all()
        )

    @admin.display(description='Собранная сумма')
    def display_current_amount(self, obj):
        """Добавляет общую сумму в разделе сбора."""
        return obj.total_amount or Decimal('0.00')

    @admin.display(description='Пожертвовавшие')
    def display_patrician_count(self, obj):
        """Добавляет количество пожертвовавших в разделе сбора."""
        return obj.uniq_patrician

    @admin.display(description='Обложка')
    def cover_tag(self, obj):
        """Добавляет обложку в разделе сбора."""
        if obj.cover:
            return mark_safe(
                f'<img src={obj.cover.url} width="60" height="60">'
            )
        return 'Нет изображения'
