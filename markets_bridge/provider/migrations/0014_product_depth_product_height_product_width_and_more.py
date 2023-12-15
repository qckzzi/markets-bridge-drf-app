# Generated by Django 4.2.6 on 2023-12-10 16:02

from decimal import (
    Decimal,
)

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0013_product_warehouse'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='depth',
            field=models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=6, verbose_name='Глубина, см'),
        ),
        migrations.AddField(
            model_name='product',
            name='height',
            field=models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=6, verbose_name='Высота, см'),
        ),
        migrations.AddField(
            model_name='product',
            name='width',
            field=models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=6, verbose_name='Ширина, см'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='external_id',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='Внешний id в системе поставщика'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='category',
            name='external_id',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='Внешний id в системе маркетплейса'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='characteristic',
            name='external_id',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='Внешний id в системе маркетплейса'),
        ),
        migrations.AlterField(
            model_name='characteristic',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='characteristicvalue',
            name='external_id',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='Внешний id в системе поставщика'),
        ),
    ]