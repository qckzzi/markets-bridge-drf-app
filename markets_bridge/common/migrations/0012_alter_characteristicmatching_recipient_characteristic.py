# Generated by Django 4.2.6 on 2023-11-15 11:22

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('recipient', '0008_alter_category_parent_category_and_more'),
        ('common', '0011_alter_systemsettingconfig_vat_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteristicmatching',
            name='recipient_characteristic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipient.characteristicforcategory', verbose_name='Характеристика получателя'),
        ),
    ]