# Generated by Django 4.2.6 on 2023-11-14 13:52

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('recipient', '0006_alter_characteristicvalue_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteristicvalue',
            name='external_id',
            field=models.PositiveIntegerField(verbose_name='Внешний id в системе получателя'),
        ),
    ]