# Generated by Django 4.2.6 on 2023-11-13 15:24

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0008_alter_product_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='markup',
            field=models.PositiveIntegerField(default=0, verbose_name='Коэффициент наценки стоимости товара, %'),
        ),
    ]
