# Generated by Django 4.2.6 on 2023-12-28 14:49

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('recipient', '0008_alter_category_parent_category_and_more'),
        ('provider', '0015_alter_product_depth_alter_product_height_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='characteristicvalue',
            name='recipient_characteristic_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='provider_characteristic_values', to='recipient.characteristicvalue', verbose_name='Значение характеристики в системе получателя'),
        ),
    ]
