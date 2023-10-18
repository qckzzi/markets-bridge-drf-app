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
