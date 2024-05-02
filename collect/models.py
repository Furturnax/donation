from django.db import models
from django.core.validators import MinValueValidator

from core.consts import (
    DECIMAL_PLACE,
    MAX_DIGITS_DECIMALFIELD,
    MAX_LENGHT_TITLE,
    MAX_LENGTH_TEXT,
    MIN_PAYMENT,
    MIN_VALUE_VALIDATOR
)
from users.models import User


class Collect(models.Model):
    """Модель сбора."""

    author = models.ForeignKey(
        User, verbose_name='Автор сбора', on_delete=models.CASCADE,
    )
    title = models.CharField(
        'Название сбора', max_length=MAX_LENGHT_TITLE,
    )
    event = models.ManyToManyField(
        'Event', verbose_name='Событие',
    )
    text = models.TextField(
        'Описание целей сбора',
        max_length=MAX_LENGTH_TEXT,
    )
    target_amount = models.IntegerField(
        'Сумма запланированная к сбору',
        default=None,
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
    cover = models.ImageField(
        'Обложка сбора', upload_to='source/image/', null=True, blank=True
    )
    endtime = models.DateTimeField(
        'Дата и время завершение сбора',
    )
    created_at = models.DateTimeField(
        'Время создания сбора', auto_now_add=True
    )

    class Meta:
        verbose_name = 'сбор'
        verbose_name_plural = 'Сборы'
        ordering = ('title',)

    def __str__(self):
        return f'{self.title} - {self.author.username} - {self.target_amount}'


class Event(models.Model):
    """Модель события для сбора."""

    title = models.CharField(
        'Событие для сбора', max_length=MAX_LENGHT_TITLE,
    )

    class Meta:
        verbose_name = 'событие сбора'
        verbose_name_plural = 'События сборов'

    def __str__(self):
        return f'{self.title}'


class Payment(models.Model):
    """Модель платежа."""

    collect = models.ForeignKey(
        Collect, verbose_name='Платеж сбора', on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User, verbose_name='Пользователь платежа', on_delete=models.CASCADE,
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
    created_at = models.DateTimeField(
        'Время поступления платежа', auto_now_add=True,
    )

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'Платяжи'
        ordering = ('-created_at',)
        default_related_name = 'payments'

    def __str__(self):
        return (
            f'{self.user.username} жертвует {self.amount} '
            f'в {self.created_at}'
        )
