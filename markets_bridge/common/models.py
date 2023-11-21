from decimal import (
    Decimal,
)

from django.db import (
    models,
)

from common.enums import (
    MarketplaceTypeEnum,
    VatRate,
)


class Marketplace(models.Model):
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
        null=True,
        related_name='marketplaces',
    )
    type = models.PositiveSmallIntegerField(
        verbose_name='Тип',
        choices=MarketplaceTypeEnum.get_choices(),
    )
    logistics = models.ForeignKey(
        'common.Logistics',
        on_delete=models.PROTECT,
        verbose_name='Логистика',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name} (ID: {self.pk})'

    class Meta:
        verbose_name = 'Маркетплейс'
        verbose_name_plural = 'Маркетплейсы'


class Currency(models.Model):
    name = models.CharField(verbose_name='Наименование валюты', max_length=100)
    code = models.CharField(verbose_name='Код валюты', max_length=3)

    def __str__(self):
        return f'{self.name} ({self.code})'

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class Logistics(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование',
    )
    cost = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        verbose_name='Стоимость за кг',
        default=Decimal('0.00'),
    )
    currency = models.ForeignKey(
        'common.Currency',
        on_delete=models.PROTECT,
        verbose_name='Валюта',
        related_name='logistics',
    )

    @property
    def currency_code(self):
        return self.currency.code

    class Meta:
        verbose_name = 'Логистика'
        verbose_name_plural = 'Логистика'

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    source = models.ForeignKey(
        'common.Currency',
        on_delete=models.CASCADE,
        verbose_name='Исходная валюта',
        related_name='source_exchange_rates'
    )
    destination = models.ForeignKey(
        'common.Currency',
        on_delete=models.CASCADE,
        verbose_name='Валюта назначения',
        related_name='destination_exchange_rate'
    )
    rate = models.DecimalField(
        decimal_places=4,
        max_digits=10,
        verbose_name='Курс',
    )
    rate_datetime = models.DateTimeField(
        verbose_name='Последнее время обновления курса',
    )

    def __str__(self):
        return f'{self.source} | {self.destination}'

    class Meta:
        verbose_name = 'Курс валют'
        verbose_name_plural = 'Курсы валют'


class SystemSettingConfig(models.Model):
    vat_rate = models.CharField(
        verbose_name='Ставка НДС',
        choices=VatRate.get_choices(),
        default=VatRate.NON_TAXABLE,
    )
    is_selected = models.BooleanField(
        verbose_name='Активная конфигурация',
        default=False,
    )

    def save(self, *args, **kwargs):
        """При выборе записи метод деактивирует выбор всех конфигураций.
        Это создает ограничение на выбор нескольких записей конфигураций.
        """

        if self.is_selected:
            SystemSettingConfig.objects.exclude(pk=self.pk).update(is_selected=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Конфигурация системы №{self.pk}'

    class Meta:
        verbose_name = 'Конфигурация системы'
        verbose_name_plural = 'Конфигурации системы'


class CategoryMatching(models.Model):
    provider_category = models.OneToOneField(
        'provider.Category',
        on_delete=models.CASCADE,
        related_name='matching',
        verbose_name='Категория поставщика',
    )
    recipient_category = models.ForeignKey(
        'recipient.Category',
        on_delete=models.SET_NULL,
        related_name='matchings',
        verbose_name='Категория получателя',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.provider_category} | {self.recipient_category or "Нет сопоставления"}'

    class Meta:
        verbose_name = 'Сопоставление категорий'
        verbose_name_plural = 'Сопоставления категорий'


class CharacteristicMatching(models.Model):
    category_matching = models.ForeignKey(
        'common.CategoryMatching',
        on_delete=models.CASCADE,
        related_name='characteristic_matchings',
        verbose_name='Сопоставление категорий',
    )
    recipient_characteristic = models.ForeignKey(
        'recipient.CharacteristicForCategory',
        on_delete=models.CASCADE,
        verbose_name='Характеристика получателя',
    )
    provider_characteristic = models.ForeignKey(
        'provider.Characteristic',
        on_delete=models.SET_NULL,
        verbose_name='Характеристика поставщика',
        null=True,
        blank=True,
    )
    recipient_value = models.ForeignKey(
        'recipient.CharacteristicValue',
        on_delete=models.SET_NULL,
        related_name='characteristic_matchings',
        verbose_name='Значение в системе получателя',
        null=True,
        blank=True,
    )
    value = models.CharField(
        max_length=255,
        verbose_name='"Сырое" значение',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.recipient_characteristic} | {self.provider_characteristic or "Нет сопоставления"}'

    class Meta:
        verbose_name = 'Сопоставление характеристик'
        verbose_name_plural = 'Сопоставления характеристик'


class CharacteristicValueMatching(models.Model):
    characteristic_matching = models.ForeignKey(
        'common.CharacteristicMatching',
        on_delete=models.CASCADE,
        related_name='value_matchings',
        verbose_name='Сопоставление характеристик',
    )
    recipient_characteristic_value = models.ForeignKey(
        'recipient.CharacteristicValue',
        on_delete=models.CASCADE,
        related_name='matchings',
        verbose_name='Значение получателя',
    )
    provider_characteristic_value = models.ForeignKey(
        'provider.CharacteristicValue',
        on_delete=models.SET_NULL,
        related_name='matchings',
        verbose_name='Значение поставщика',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.recipient_characteristic_value} | {self.provider_characteristic_value or "Нет сопоставления"}'

    class Meta:
        verbose_name = 'Сопоставление значений характеристик'
        verbose_name_plural = 'Сопоставления значений характеристик'


class Log(models.Model):
    service_name = models.CharField(
        max_length=255,
        verbose_name='Наименование сервиса',
    )
    entry = models.TextField(
        verbose_name='Запись',
    )
    timestamp = models.DateTimeField(
        verbose_name='Timestamp',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Логи'
        verbose_name_plural = 'Записи в логах'

    def __str__(self):
        return f'{self.service_name} log (ID: {self.pk})'


class SystemEnvironment(models.Model):
    key = models.CharField(
        max_length=255,
        verbose_name='Ключ',
        primary_key=True,
        unique=True,
    )
    value = models.TextField(
        verbose_name='Значение',
    )

    class Meta:
        verbose_name = 'Системная переменная'
        verbose_name_plural = 'Системные переменные'

    def __str__(self):
        return f'{self.key}: {self.value}'
