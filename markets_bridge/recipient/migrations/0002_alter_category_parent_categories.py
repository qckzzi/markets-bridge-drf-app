# Generated by Django 4.2.6 on 2023-10-27 19:22

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('recipient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent_categories',
            field=models.ManyToManyField(blank=True, null=True, related_name='children', to='recipient.category', verbose_name='Родительские категории'),
        ),
    ]
