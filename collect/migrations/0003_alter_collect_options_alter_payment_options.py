# Generated by Django 5.0.4 on 2024-05-06 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collect',
            options={'default_related_name': 'collects', 'verbose_name': 'сбор', 'verbose_name_plural': 'Сборы'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'default_related_name': 'payments', 'verbose_name': 'платеж', 'verbose_name_plural': 'Платяжи'},
        ),
    ]
