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
    parent_categories = models.ManyToManyField(
        'self',
        verbose_name='Родительские категории',
        related_name='children',
        symmetrical=False,
        blank=True,
    )
    marketplace = models.ForeignKey(
        'common.Marketplace',
        verbose_name='Маркетплейс-получатель',
        on_delete=models.PROTECT,
        related_name='recipient_categories',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория в системе получателя'
        verbose_name_plural = 'Категории в системе получателя'


class Characteristic(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний id в системе получателя',
        db_index=True,
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
    )
    is_required = models.BooleanField(
        verbose_name='Обязательная характеристика',
        default=False,
    )
    categories = models.ManyToManyField(
        'recipient.Category',
        verbose_name='Категории в системе получателя',
        related_name='characteristics',
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
        db_index=True,
    )
    value = models.CharField(
        verbose_name='Значение',
        max_length=200,
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
        return self.value

    class Meta:
        verbose_name = 'Значение характеристики в системе получателя'
        verbose_name_plural = 'Значения характеристики в системе получателя'
