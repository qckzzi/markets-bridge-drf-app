from django.contrib import (
    admin,
)

from common.models import (
    Currency,
)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass
