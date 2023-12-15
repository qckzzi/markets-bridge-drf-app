# Generated by Django 4.2.6 on 2023-12-03 18:07

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_personalarea_personalareavariable_systemvariable_and_more'),
        ('provider', '0012_alter_product_markup'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='common.warehouse', verbose_name='Склад'),
        ),
    ]