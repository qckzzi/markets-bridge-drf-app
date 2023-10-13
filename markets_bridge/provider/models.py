from decimal import (
    Decimal,
)

from django.db import (
    models,
)


class ProviderMarketplace(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    url = models.URLField(
        verbose_name='URL маркетплейса',
    )
    currency = models.ForeignKey(
        'common.Currency',
        verbose_name='Валюта',
        on_delete=models.PROTECT,
        related_name='provider_marketplaces',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маркетплейс-поставщик'
        verbose_name_plural = 'Маркетплейсы-поставщики'


class ProviderCategory(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    translated_name = models.CharField(
        verbose_name='Переведённое наименование',
        max_length=100,
        null=True,
        blank=True,
    )
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе маркетплейса',
        db_index=True,
        unique=True,
    )
    provider_marketplace = models.ForeignKey(
        'provider.ProviderMarketplace',
        verbose_name='Маркетплейс-поставщик',
        on_delete=models.PROTECT,
        related_name='categories',
    )

    def __str__(self):
        return f'{self.name} ({self.translated_name or "Перевод отсутствует"})'

    class Meta:
        verbose_name = 'Категория с системе поставщика'
        verbose_name_plural = 'Категории в системе поставщика'


class ProviderCharacteristic(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    translated_name = models.CharField(
        verbose_name='Переведённое наименование',
        max_length=100,
        null=True,
        blank=True,
    )
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе маркетплейса',
    )
    provider_category = models.ManyToManyField(
        'provider.ProviderCategory',
        verbose_name='Категории в системе поставщика',
        related_name='characteristics',
    )

    def __str__(self):
        return f'{self.name} ({self.translated_name or "Перевод отсутствует"})'

    class Meta:
        verbose_name = 'Характеристика товара с системе поставщика'
        verbose_name_plural = 'Характеристики товара в системе поставщика'


class ProviderCharacteristicValue(models.Model):
    value = models.CharField(
        verbose_name='Значение',
        max_length=200,
    )
    translated_value = models.CharField(
        verbose_name='Переведённое значение',
        max_length=100,
        null=True,
        blank=True,
    )
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе поставщика',
    )
    provider_characteristic = models.ForeignKey(
        'provider.ProviderCharacteristic',
        verbose_name='Характеристика в системе поставщика',
        on_delete=models.CASCADE,
        related_name='characteristics',
    )

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.value} ({self.translated_value or "Перевод отсутствует"})'

    class Meta:
        verbose_name = 'Значение характеристики в системе поставщика'
        verbose_name_plural = 'Значения характеристики в системе поставщика'


class ProductCharacteristicValue(models.Model):
    scrapped_product = models.ForeignKey(
        'provider.ScrappedProduct',
        on_delete=models.CASCADE,
        related_name='characteristic_values',
        verbose_name='Товар',
    )
    provider_characteristic_value = models.ForeignKey(
        'provider.ProviderCharacteristicValue',
        on_delete=models.CASCADE,
        related_name='product_values',
        verbose_name='Значение характеристики в системе поставщика',
    )


class ScrappedProduct(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    translated_name = models.CharField(
        verbose_name='Переведённое наименование',
        max_length=100,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        default='',
        null=True,
        blank=True,
    )
    translated_description = models.TextField(
        verbose_name='Переведенное описание',
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    import_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True,
    )
    upload_date = models.DateTimeField(
        verbose_name='Дата выгрузки',
        null=True,
        blank=True,
    )
    status = models.BooleanField(
        verbose_name='Разрешение для экспорта',
        default=False,
    )
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе поставщика',
    )
    provider_category = models.ForeignKey(
        'provider.ProviderCategory',
        verbose_name='Категория в системе поставщика',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products',
    )

    def __str__(self):
        return f'{self.name} ({self.translated_name or "Перевод отсутствует"})'

    class Meta:
        verbose_name = 'Спаршенный товар'
        verbose_name_plural = 'Спаршенные товары'


def collect_image_path(instance, filename):
    return f'{instance.product.provider_category_id}/{instance.product.id}/{filename}'


class ProductImage(models.Model):
    image = models.ImageField(
        verbose_name='Изображение товара',
        upload_to=collect_image_path,
    )
    product = models.ForeignKey(
        'provider.ScrappedProduct',
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='images',
    )

    def __str__(self):
        return f'{self.image.name} ({self.product.name}'

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'


def unpack_categories(categories):
    result = []
    for category in categories:
        if category["subCategories"]:
            result.extend(unpack_categories(category["subCategories"]))
        else:
            category_instance = ProviderCategory(
                external_id=category["id"],
                name=category["name"],
                provider_marketplace_id=1,
            )
            result.append(category_instance)

    return result
