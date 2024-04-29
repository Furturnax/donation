from django.db import models
from django.core.validators import MinValueValidator

from core.consts import (
    DECIMAL_PLACE,
    MAX_DIGITS_DECIMALFIELD,
    MAX_LENGHT_TITLE,
    MIN_PAYMENT,
    MIN_VALUE_VALIDATOR
)
from users.models import User


class Occasion(models.Model):
    """Модель причин сбора."""

    title = models.CharField(
        'Повод для сбора',
        max_length=MAX_LENGHT_TITLE,
    )

    class Meta:
        verbose_name = 'причина сбора'
        verbose_name_plural = 'Причины сборов'
        ordering = ('title',)

    def __str__(self):
        return f'{self.title}'


class Collect(models.Model):
    """Модель сбора."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор сбора',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        'Название сбора',
        max_length=MAX_LENGHT_TITLE,
    )
    occasion = models.ManyToManyField(
        Occasion,
        verbose_name='Причина',
    )
    description = models.TextField(
        'Описание целей сбора',
    )
    target_amount = models.DecimalField(
        'Сумма запланированная к сбору',
        max_digits=MAX_DIGITS_DECIMALFIELD,
        decimal_places=DECIMAL_PLACE,
        validators=(
            MinValueValidator(
                MIN_VALUE_VALIDATOR,
                message=(
                    'Минимально заплонированная сумма '
                    f'сбора - {MIN_VALUE_VALIDATOR}.'
                )
            ),
        ),
    )
    current_amount = models.DecimalField(
        'Собранная сумма на текущий момент',
        max_digits=MAX_DIGITS_DECIMALFIELD,
        decimal_places=DECIMAL_PLACE,
        validators=(
            MinValueValidator(
                MIN_VALUE_VALIDATOR,
                message=(
                    'Минимально собранная сумма '
                    f'сбора - {MIN_VALUE_VALIDATOR}.'
                )
            ),
        ),
    )
    contributors_count = models.PositiveIntegerField(
        'Колличество сделавших пожертвование',
        validators=(
            MinValueValidator(
                MIN_VALUE_VALIDATOR,
                message=(
                    'Минимальное количество людей сделавших '
                    f'пожертование - {MIN_VALUE_VALIDATOR}.'
                )
            ),
        ),
    )
    cover_image = models.ImageField(
        'Обложка сбора',
        upload_to='source/image/',
    )
    end_datetime = models.DateTimeField(
        'Дата и время завершение сбора',
    )

    class Meta:
        verbose_name = 'сбор'
        verbose_name_plural = 'Сборы'
        ordering = ('title',)

    def __str__(self):
        return f'{self.title} - {self.author.username} - {self.target_amount}'


class Payment(models.Model):
    """Модель платежа."""

    collect = models.ForeignKey(
        Collect,
        verbose_name='Платеж определенного сбора',
        on_delete=models.CASCADE,
        related_name='payments',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь оставивший платеж',
        on_delete=models.CASCADE,
        related_name='payments',
    )
    amount = models.DecimalField(
        'Сумма платежа',
        max_digits=MAX_DIGITS_DECIMALFIELD,
        decimal_places=DECIMAL_PLACE,
        validators=(
            MinValueValidator(
                MIN_PAYMENT,
                message=(
                    'Минимальная сумма платежа '
                    f'- {MIN_PAYMENT}.'
                )
            ),
        ),
    )
    datetime = models.DateTimeField(
        'Время платежа',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'Платяжи'
        ordering = ('-datetime',)

    def __str__(self):
        return (
            f'{self.user.username} жертвует {self.amount} в {self.datetime}'
        )
