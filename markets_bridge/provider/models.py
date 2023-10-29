from decimal import (
    Decimal,
)

from django.db import (
    models,
)


class Category(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе маркетплейса',
        db_index=True,
    )
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
    marketplace = models.ForeignKey(
        'common.Marketplace',
        verbose_name='Маркетплейс-поставщик',
        on_delete=models.PROTECT,
        related_name='provider_categories',
    )
    recipient_category = models.ForeignKey(
        'recipient.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='provider_categories',
        verbose_name='Категория получателя',
    )

    @property
    def name_and_translate(self):
        return f'{self.name} ({self.translated_name or "Перевод отсутствует"})'

    def __str__(self):
        return self.name_and_translate

    class Meta:
        verbose_name = 'Категория с системе поставщика'
        verbose_name_plural = 'Категории в системе поставщика'


class Characteristic(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе маркетплейса',
        db_index=True,
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255,
    )
    translated_name = models.CharField(
        verbose_name='Переведённое наименование',
        max_length=255,
        null=True,
        blank=True,
    )
    is_required = models.BooleanField(
        verbose_name='Обязательная характеристика',
        default=False,
    )
    categories = models.ManyToManyField(
        'provider.Category',
        verbose_name='Категории в системе поставщика',
        related_name='characteristics',
    )
    recipient_characteristic = models.ForeignKey(
        'recipient.Characteristic',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='provider_characteristics',
        verbose_name='Характеристика в системе поставщика',
    )

    @property
    def name_and_translate(self):
        return f'{self.name} ({self.translated_name or "Перевод отсутствует"})'

    def __str__(self):
        return self.name_and_translate

    class Meta:
        verbose_name = 'Характеристика товара с системе поставщика'
        verbose_name_plural = 'Характеристики товара в системе поставщика'


class CharacteristicValue(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе поставщика',
        db_index=True,
    )
    value = models.CharField(
        verbose_name='Значение',
        max_length=255,
    )
    translated_value = models.CharField(
        verbose_name='Переведённое значение',
        max_length=255,
        null=True,
        blank=True,
    )
    characteristic = models.ForeignKey(
        'provider.Characteristic',
        verbose_name='Характеристика в системе поставщика',
        on_delete=models.CASCADE,
        related_name='characteristic_values',
    )
    recipient_characteristic_value = models.ForeignKey(
        'recipient.CharacteristicValue',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='provider_characteristic_values',
        verbose_name='Значение характеристики в системе поставщика',
    )

    @property
    def value_and_translate(self):
        return f'{self.value} ({self.translated_value or "Перевод отсутствует"})'

    def __str__(self):
        return self.value_and_translate

    class Meta:
        verbose_name = 'Значение характеристики в системе поставщика'
        verbose_name_plural = 'Значения характеристики в системе поставщика'


class Product(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе поставщика',
        db_index=True,
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255,
    )
    translated_name = models.CharField(
        verbose_name='Переведённое наименование',
        max_length=255,
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
    url = models.URLField(
        verbose_name='URL товара',
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    discounted_price = models.DecimalField(
        verbose_name='Цена со скидкой',
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
    category = models.ForeignKey(
        'provider.Category',
        verbose_name='Категория в системе поставщика',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products',
    )
    characteristic_values = models.ManyToManyField(
        'provider.CharacteristicValue',
        verbose_name='Значение характеристики в системе поставщика',
        related_name='products',
        through='ProductValue',
    )

    @property
    def name_and_translate(self):
        return f'{self.name} ({self.translated_name or "Перевод отсутствует"})'

    def __str__(self):
        return self.name_and_translate

    class Meta:
        verbose_name = 'Товар с системе поставщика'
        verbose_name_plural = 'Товары с системе поставщика'


class ProductValue(models.Model):
    product = models.ForeignKey(
        'provider.Product',
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )
    value = models.ForeignKey(
        'provider.CharacteristicValue',
        on_delete=models.CASCADE,
        verbose_name='Значение',
    )


def collect_image_path(instance, filename):
    return (
        f'{instance.product.category_id}/{instance.product.pk}/{filename}'
    )


class ProductImage(models.Model):
    image = models.ImageField(
        verbose_name='Изображение товара',
        upload_to=collect_image_path,
    )
    product = models.ForeignKey(
        'provider.Product',
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='images',
    )

    def __str__(self):
        return f'{self.image.name} ({self.product.name}'

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'
