from django.db import models


class RawCategory(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    url = models.URLField(
        verbose_name='URL товара',
    )
    status = models.BooleanField(
        verbose_name='Разрешение для импорта',
    )
    provider_category = models.ForeignKey(
        'provider.ProviderCategory',
        verbose_name='Категория в системе поставщика',
        null=True,
        on_delete=models.SET_NULL,
        related_name='row_categories',
    )

    def __repr__(self):
        return f'{self.__str__()} (id: {self.id})'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сырая категория'
        verbose_name_plural = 'Сырые категории'


class RawProduct(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    url = models.URLField(
        verbose_name='URL товара',
    )
    status = models.BooleanField(
        verbose_name='Разрешение для импорта',
    )
    raw_category = models.ForeignKey(
        'parser_targets.RawCategory',
        verbose_name='Сырая категория',
        null=True,
        on_delete=models.SET_NULL,
        related_name='raw_products',
    )

    def __repr__(self):
        return f'{self.__str__()} (id: {self.id})'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сырой продукт'
        verbose_name_plural = 'Сырые продукты'
