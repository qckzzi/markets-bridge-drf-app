from decimal import (
    Decimal,
)

from django.db import (
    models,
)

from common.models import (
    CategoryMatching,
)
from common.services import (
    get_default_markup,
)


class Category(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе маркетплейса',
        db_index=True,
        default=0,
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
        db_index=True,
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
        default=0,
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255,
        db_index=True,
    )
    translated_name = models.CharField(
        verbose_name='Переведённое наименование',
        max_length=255,
        null=True,
        blank=True,
    )
    categories = models.ManyToManyField(
        'provider.Category',
        verbose_name='Категории в системе поставщика',
        related_name='characteristics',
    )
    marketplace = models.ForeignKey(
        'common.Marketplace',
        verbose_name='Маркетплейс-поставщик',
        on_delete=models.PROTECT,
        related_name='provider_characteristics',
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
        default=0,
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
    marketplace = models.ForeignKey(
        'common.Marketplace',
        verbose_name='Маркетплейс-поставщик',
        on_delete=models.PROTECT,
        related_name='provider_characteristic_values',
    )
    recipient_characteristic_values = models.ManyToManyField(
        'recipient.CharacteristicValue',
        verbose_name='Значения характеристики в системе получателя',
        related_name='provider_characteristic_values',
        blank=True,
    )

    @property
    def value_and_translate(self):
        return f'{self.value} ({self.translated_value or "Перевод отсутствует"})'

    def __str__(self):
        return self.value_and_translate

    class Meta:
        verbose_name = 'Значение характеристики в системе поставщика'
        verbose_name_plural = 'Значения характеристик в системе поставщика'


class Brand(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе поставщика',
        db_index=True,
        default=0,
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255,
        db_index=True,
    )
    marketplace = models.ForeignKey(
        'common.Marketplace',
        verbose_name='Маркетплейс-поставщик',
        on_delete=models.PROTECT,
        related_name='provider_brands',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд в системе поставщика'
        verbose_name_plural = 'Бренды с системе поставщика'


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
    product_code = models.CharField(
        max_length=255,
        verbose_name='Код товара',
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
        default='',
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(
        'provider.Brand',
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name='Бренд',
        null=True,
        blank=True,
    )
    url = models.URLField(
        verbose_name='URL товара',
        max_length=3000,
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
    markup = models.PositiveIntegerField(
        verbose_name='Коэффициент наценки стоимости товара, %',
        blank=True,
    )
    stock_quantity = models.IntegerField(
        verbose_name='Количество в наличии',
        default=0,
    )
    weight = models.DecimalField(
        verbose_name='Вес товара, кг',
        decimal_places=3,
        max_digits=6,
        default=Decimal('0.000'),
    )
    width = models.DecimalField(
        verbose_name='Ширина, см',
        decimal_places=1,
        max_digits=6,
        default=Decimal('0.0'),
    )
    height = models.DecimalField(
        verbose_name='Высота, см',
        decimal_places=1,
        max_digits=6,
        default=Decimal('0.0'),
    )
    depth = models.DecimalField(
        verbose_name='Глубина, см',
        decimal_places=1,
        max_digits=6,
        default=Decimal('0.0'),
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
    is_export_allowed = models.BooleanField(
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
        through='provider.ProductValue',
    )
    marketplace = models.ForeignKey(
        'common.Marketplace',
        verbose_name='Маркетплейс-поставщик',
        on_delete=models.PROTECT,
        related_name='provider_products',
    )
    is_updated = models.BooleanField(
        verbose_name='Обновлять актуальные данные от поставщика',
        default=True,
    )
    warehouse = models.ForeignKey(
        'common.Warehouse',
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name='Склад',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name_and_translate

    @property
    def name_and_translate(self):
        return f'{self.name} ({self.translated_name or "Перевод отсутствует"})'

    @property
    def currency_code(self):
        return self.marketplace.currency.code

    @property
    def logistics_currency_code(self):
        return self.marketplace.logistics.currency.code

    @property
    def vendor_code(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.markup:
            self.markup = get_default_markup()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар в системе поставщика'
        verbose_name_plural = 'Товары в системе поставщика'


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

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'
