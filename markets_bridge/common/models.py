from django.db import (
    models,
)


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


# class CategoryMatching(models.Model):
#     provider_category = models.ForeignKey(
#         'provider.ProviderCategory',
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='matchings',
#         verbose_name='Категория поставщика',
#     )
#     recipient_category = models.ForeignKey(
#         'recipient.RecipientProductType',
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='matchings',
#         verbose_name='Категория получателя',
#     )

#     def __str__(self):
#         return (
#             f'{self.provider_category or "Не указано"} = {self.recipient_category or "Не указано"}'
#         )
    
#     class Meta:
#         verbose_name = 'Соответсвие категорий'
#         verbose_name_plural = 'Соответсвия категорий'
