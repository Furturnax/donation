from django.db import models
from django.core.validators import MinValueValidator

from core.consts import (
    DECIMAL_PLACE,
    MAX_DIGITS_IN_DECIMAL,
    MAX_LENGHT_TITLE,
    MIN_VALUE_VALIDATOR
)
from users.models import User


class Collect(models.Model):
    """Модель сбора."""

    author = models.ForeignKey(
        User, verbose_name='Автор', on_delete=models.CASCADE,
    )
    title = models.CharField(
        'Название'
    )
    event = models.ManyToManyField(
        'Event', verbose_name='Событие',
    )
    text = models.TextField(
        'Описание'
    )
    target_amount = models.DecimalField(
        'Сумма',
        max_digits=MAX_DIGITS_IN_DECIMAL,
        decimal_places=DECIMAL_PLACE,
        default=None,
        validators=(
            MinValueValidator(
                MIN_VALUE_VALIDATOR,
                message=(
                    'Минимально заплонированная сумма '
                    f'сбора в рублях - {MIN_VALUE_VALIDATOR}.'
                )
            ),
        ),
    )
    cover = models.ImageField(
        'Обложка', upload_to='image/', null=True, blank=True
    )
    endtime = models.DateTimeField(
        'Дата завершение сбора',
    )
    created_at = models.DateTimeField(
        'Дата создания сбора', auto_now_add=True
    )

    class Meta:
        verbose_name = 'сбор'
        verbose_name_plural = 'Сборы'
        default_related_name = 'collects'

    def __str__(self):
        return f'{self.pk}'


class Event(models.Model):
    """Модель события для сбора."""

    title = models.CharField(
        'Событие', max_length=MAX_LENGHT_TITLE,
    )

    class Meta:
        verbose_name = 'событие сбора'
        verbose_name_plural = 'События сборов'

    def __str__(self):
        return f'{self.title}'


class Payment(models.Model):
    """Модель платежа."""

    collect = models.ForeignKey(
        Collect, verbose_name='Сбор', on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=MAX_DIGITS_IN_DECIMAL,
        decimal_places=DECIMAL_PLACE,
        validators=(
            MinValueValidator(
                MIN_VALUE_VALIDATOR,
                message=(
                    'Минимальная сумма платежа в рублях'
                    f'- {MIN_VALUE_VALIDATOR}.'
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
        default_related_name = 'payments'

    def __str__(self):
        return (f'{self.amount}')
