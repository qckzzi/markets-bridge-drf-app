# Generated by Django 4.2.6 on 2023-11-20 20:16

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0010_product_weight_alter_product_markup'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_updated',
            field=models.BooleanField(default=True, verbose_name='Обновлять актуальные данные от поставщика'),
        ),
    ]
