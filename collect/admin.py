from django.contrib import admin

from .models import Collect, Occasion, Payment


@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
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
        'datetime',
    )
    search_fields = ('user__username',)
    list_filter = (
        'user__username',
        'collect__title',
    )
    list_display_links = ('user',)
    ordering = ('user',)


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    """Интерфейс управления сборами."""

    list_display = (
        'author',
        'title',
        'display_occasion',
        'description',
        'target_amount',
        'current_amount',
        'contributors_count',
        'cover_image',
        'end_datetime',
    )
    search_fields = (
        'user__username',
        'recipe__name',
    )
    list_filter = (
        'author__username',
    )
    list_display_links = ('author',)
    ordering = ('author',)

    @admin.display(description='Теги')
    def display_occasion(self, obj):
        """Добавляет теги в разделе рецепты."""
        return ', '.join(
            occasion.title for occasion in obj.occasion.all()
        )
