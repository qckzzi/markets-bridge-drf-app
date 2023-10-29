from decimal import (
    Decimal,
)

from django.db import (
    models,
)

from common.enums import (
    MarketplaceTypeEnum,
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
        on_delete=models.SET_NULL,
        null=True,
        related_name='marketplaces',
    )
    type = models.PositiveSmallIntegerField(
        verbose_name='Тип',
        choices=MarketplaceTypeEnum.get_choices(),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маркетплейс'
        verbose_name_plural = 'Маркетплейсы'


class Currency(models.Model):
    name = models.CharField(verbose_name='Наименование валюты', max_length=100)
    code = models.CharField(verbose_name='Код валюты', max_length=3)

    def __repr__(self):
        return f'{self.__str__()} (id: {self.id})'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class SystemSettingConfig(models.Model):
    markup = models.DecimalField(
        verbose_name='Коэффициент наценки стоимости товаров',
        max_digits=3,
        decimal_places=2,
        default=Decimal('1.00'),
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
