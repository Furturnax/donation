# Generated by Django 5.0.4 on 2024-05-03 13:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0004_alter_collect_text_alter_collect_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collect',
            name='target_amount',
            field=models.PositiveIntegerField(default=None, validators=[django.core.validators.MinValueValidator(1, message='Минимально заплонированная сумма сбора в рублях - 1.')], verbose_name='Сумма запланированная к сбору'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальная сумма платежа в рублях- 1.')], verbose_name='Сумма платежа'),
        ),
    ]
