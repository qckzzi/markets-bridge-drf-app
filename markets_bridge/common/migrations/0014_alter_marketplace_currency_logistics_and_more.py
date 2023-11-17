# Generated by Django 4.2.6 on 2023-11-16 19:16

from decimal import (
    Decimal,
)

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_exchangerate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplace',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='marketplaces', to='common.currency', verbose_name='Валюта'),
        ),
        migrations.CreateModel(
            name='Logistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8, verbose_name='Стоимость за кг')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logistics', to='common.currency', verbose_name='Валюта')),
            ],
            options={
                'verbose_name': 'Логистика',
                'verbose_name_plural': 'Логистика',
            },
        ),
        migrations.AddField(
            model_name='marketplace',
            name='logistics',
            field=models.ForeignKey(blank=True, null=True, default=None, on_delete=django.db.models.deletion.PROTECT, to='common.logistics', verbose_name='Логистика'),
            preserve_default=False,
        ),
    ]