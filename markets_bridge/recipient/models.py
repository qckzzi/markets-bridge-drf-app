from django.db import (
    models,
)


class RecipientMarketplace(models.Model):
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
        related_name='recipient_marketplaces',
    )

    def __repr__(self):
        return f'{self.__str__()} (id: {self.id})'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маркетплейс-получатель'
        verbose_name_plural = 'Маркетплейсы-получатели'


class RecipientCategory(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе маркетплейса',
        db_index=True,
        unique=True,
    )
    parent_categories = models.ManyToManyField(
        'self',
        verbose_name='Родительские категории',
    )
    recipient_marketplace = models.ForeignKey(
        'recipient.RecipientMarketplace',
        verbose_name='Маркетплейс-получатель',
        on_delete=models.PROTECT,
        related_name='categories',
    )

    def __repr__(self):
        return f'{self.__str__()} (id: {self.id})'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория в системе получателя'
        verbose_name_plural = 'Категории в системе получателя'


class RecipientCharacteristic(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе получателя',
        unique=True,
    )
    is_required = models.BooleanField(
        verbose_name='Обязательная характеристика',
        default=False,
    )
    recipient_category = models.ManyToManyField(
        'recipient.RecipientCategory',
        verbose_name='Категории в системе получателя',
        related_name='characteristics',
    )

    def __repr__(self):
        return f'{self.__str__()} (id: {self.id})'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристика товара с системе получателя'
        verbose_name_plural = 'Характеристики товара в системе получателя'


class RecipientCharacteristicValue(models.Model):
    value = models.CharField(
        verbose_name='Значение',
        max_length=200,
    )
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе получателя',
    )
    recipient_characteristic = models.ForeignKey(
        'recipient.RecipientCharacteristic',
        verbose_name='Характеристика в системе получателя',
        on_delete=models.CASCADE,
        related_name='characteristics',
    )

    def __repr__(self):
        return f'{self.__str__()} (id: {self.id})'

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Значение характеристики в системе получателя'
        verbose_name_plural = 'Значения характеристики в системе получателя'
