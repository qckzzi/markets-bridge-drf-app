from django.contrib import (
    admin,
)

from common.models import (
    CategoryMatching,
    CharacteristicMatching,
    CharacteristicValueMatching,
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


@admin.register(CategoryMatching)
class CategoryMatchingAdmin(admin.ModelAdmin):
    list_display = ('provider_category', 'recipient_category')
    readonly_fields = ('provider_category',)
    list_editable = ('recipient_category',)
    search_fields = ('provider_category__name', 'recipient_category__name',)
    autocomplete_fields = ('recipient_category',)

    def get_search_results(self, request, queryset, search_term):
        return super().get_search_results(request, queryset, search_term)

    list_per_page = 10


@admin.register(CharacteristicMatching)
class CharacteristicMatchingAdmin(admin.ModelAdmin):
    list_display = (
        'recipient_characteristic',
        'provider_characteristic',
        'value',
    )
    list_editable = (
        'provider_characteristic',
        'value',
    )
    autocomplete_fields = (
        'provider_characteristic',
    )


@admin.register(CharacteristicValueMatching)
class CharacteristicValueMatchingAdmin(admin.ModelAdmin):
    list_display = ('recipient_characteristic_value', 'provider_characteristic_value')
    list_editable = ('provider_characteristic_value',)
    autocomplete_fields = ('provider_characteristic_value',)
