from django.contrib import (
    admin,
)

from common.models import (
    Currency,
    Marketplace,
    SystemSettingConfig,
)


@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'currency', 'type')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(SystemSettingConfig)
class SystemSettingConfigAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_selected')
    list_editable = ('is_selected',)
