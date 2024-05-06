# Generated by Django 5.0.4 on 2024-05-05 16:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collect', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='collect',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='collect',
            name='event',
            field=models.ManyToManyField(to='collect.event', verbose_name='Событие'),
        ),
        migrations.AddField(
            model_name='payment',
            name='collect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collect.collect', verbose_name='Платеж сбора'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь платежа'),
        ),
    ]
