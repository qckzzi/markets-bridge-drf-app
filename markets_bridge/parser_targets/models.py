from django.db import (
    models,
)


class RawCategory(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    url = models.URLField(
        verbose_name='URL товара',
    )
    is_allowed_import = models.BooleanField(
        verbose_name='Разрешение для импорта',
        default=False,
    )
    provider_marketplace = models.ForeignKey(
        'provider.ProviderMarketplace',
        on_delete=models.CASCADE,
        related_name='raw_categories',
        verbose_name='Маркетплейс-поставщик',
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
    is_allowed_import = models.BooleanField(
        verbose_name='Разрешение для импорта',
        default=False,
    )
    provider_marketplace = models.ForeignKey(
        'provider.ProviderMarketplace',
        on_delete=models.CASCADE,
        related_name='raw_products',
        verbose_name='Маркетплейс-поставщик',
    )

    def __repr__(self):
        return f'{self.__str__()} (id: {self.id})'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сырой продукт'
        verbose_name_plural = 'Сырые продукты'
