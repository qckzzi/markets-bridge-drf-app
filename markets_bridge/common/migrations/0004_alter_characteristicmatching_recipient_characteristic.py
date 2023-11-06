# Generated by Django 4.2.6 on 2023-11-04 06:09

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('recipient', '0005_remove_category_parent_categories_and_more'),
        ('common', '0003_alter_characteristicmatching_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteristicmatching',
            name='recipient_characteristic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recipient.characteristic', verbose_name='Характеристика получателя'),
        ),
    ]