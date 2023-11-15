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
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        verbose_name='Родительская категория',
        related_name='children',
        null=True,
        blank=True,
    )
    marketplace = models.ForeignKey(
        'common.Marketplace',
        verbose_name='Маркетплейс-получатель',
        on_delete=models.PROTECT,
        related_name='recipient_categories',
    )

    def __str__(self):
        return f'{self.external_id}, {self.name}'

    class Meta:
        verbose_name = 'Категория в системе получателя'
        verbose_name_plural = 'Категории в системе получателя'


class CharacteristicForCategory(models.Model):
    category = models.ForeignKey(
        'recipient.Category',
        on_delete=models.CASCADE,
        verbose_name='Категория в системе поставщика',
    )
    characteristic = models.ForeignKey(
        'recipient.Characteristic',
        on_delete=models.CASCADE,
        verbose_name='Характеристика в системе поставщика',
    )
    is_required = models.BooleanField(
        verbose_name='Обязательная характеристика',
        default=False,
    )

    class Meta:
        verbose_name = 'Связь категория-характеристика'
        verbose_name_plural = 'Связи категория-характеристика'

    def __str__(self):
        return f'{self.characteristic}{"*" if self.is_required else ""}'


class Characteristic(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе получателя',
        db_index=True,
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание характеристики',
    )
    has_reference_values = models.BooleanField(
        default=False,
        verbose_name='Имеет ссылочные значения',
    )
    categories = models.ManyToManyField(
        'recipient.Category',
        verbose_name='Категории в системе получателя',
        related_name='characteristics',
        through='recipient.CharacteristicForCategory',
    )
    marketplace = models.ForeignKey(
        'common.Marketplace',
        on_delete=models.PROTECT,
        related_name='recipient_characteristics',
        verbose_name='Маркетплейс-получатель',
    )

    def __repr__(self):
        return f'{self.__str__()} (id: {self.id})'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристика товара с системе получателя'
        verbose_name_plural = 'Характеристики товара в системе получателя'


class CharacteristicValue(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе получателя',
    )
    value = models.TextField(
        verbose_name='Значение',
    )
    characteristic = models.ForeignKey(
        'recipient.Characteristic',
        verbose_name='Характеристика в системе получателя',
        on_delete=models.CASCADE,
        related_name='characteristic_values',
    )
    marketplace = models.ForeignKey(
        'common.Marketplace',
        on_delete=models.PROTECT,
        related_name='recipient_characteristic_values',
        verbose_name='Маркетплейс-получатель',
    )

    def __str__(self):
        return f'{self.value} ({self.characteristic.name})'

    class Meta:
        verbose_name = 'Значение характеристики в системе получателя'
        verbose_name_plural = 'Значения характеристики в системе получателя'
