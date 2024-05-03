# Generated by Django 5.0.4 on 2024-05-03 11:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название сбора')),
                ('text', models.TextField(max_length=30000, verbose_name='Описание целей сбора')),
                ('target_amount', models.IntegerField(default=None, validators=[django.core.validators.MinValueValidator(1, message='Минимально заплонированная сумма сбора - 1.')], verbose_name='Сумма запланированная к сбору')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='image/', verbose_name='Обложка сбора')),
                ('endtime', models.DateTimeField(verbose_name='Дата и время завершение сбора')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания сбора')),
            ],
            options={
                'verbose_name': 'сбор',
                'verbose_name_plural': 'Сборы',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Событие для сбора')),
            ],
            options={
                'verbose_name': 'событие сбора',
                'verbose_name_plural': 'События сборов',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0.01, message='Минимальная сумма платежа - 0.01.')], verbose_name='Сумма платежа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время поступления платежа')),
            ],
            options={
                'verbose_name': 'платеж',
                'verbose_name_plural': 'Платяжи',
                'ordering': ('-created_at',),
                'default_related_name': 'payments',
            },
        ),
    ]