# Generated by Django 4.2.6 on 2024-01-01 21:22

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0017_remove_characteristicvalue_recipient_characteristic_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='product',
            name='translated_description',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Переведенное описание'),
        ),
    ]
