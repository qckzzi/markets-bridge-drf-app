# Generated by Django 4.2.6 on 2023-11-05 09:36

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0006_remove_category_recipient_category_and_more'),
        ('common', '0006_alter_categorymatching_provider_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='characteristicmatching',
            name='recipient_value',
        ),
        migrations.AlterField(
            model_name='characteristicmatching',
            name='provider_characteristic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='provider.characteristic', verbose_name='Характеристика поставщика'),
        ),
    ]
