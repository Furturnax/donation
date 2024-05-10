from django.db import models
from django.contrib.auth.models import AbstractUser

from core.consts import LENGTH_USER_CHARFIELD, LENGTH_USER_EMAILFIELD
from core.validators import username_validator


class User(AbstractUser):
    """Модель переопределенного класса User."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    email = models.EmailField(
        'Электронная почта',
        max_length=LENGTH_USER_EMAILFIELD,
        unique=True,
        help_text=(
            'Укажите уникальный юзернейм. Может содержать до '
            f'{LENGTH_USER_EMAILFIELD} символов.'
        ),
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=LENGTH_USER_CHARFIELD,
        unique=True,
        validators=(username_validator,),
    )
    first_name = models.CharField(
        'Имя',
        max_length=LENGTH_USER_CHARFIELD,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=LENGTH_USER_CHARFIELD,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}'
