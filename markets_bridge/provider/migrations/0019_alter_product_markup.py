# Generated by Django 4.2.6 on 2024-01-16 20:34

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0018_product_description_product_translated_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='markup',
            field=models.PositiveIntegerField(blank=True, verbose_name='Коэффициент наценки стоимости товара, %'),
        ),
    ]