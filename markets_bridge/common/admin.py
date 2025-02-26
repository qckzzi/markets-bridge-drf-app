from django.contrib import (
    admin,
)
from django.urls import (
    reverse,
)
from django.utils.html import (
    format_html,
)

from common.models import (
    CategoryMatching,
    CharacteristicMatching,
    CharacteristicValueMatching,
    Currency,
    ExchangeRate,
    Log,
    Logistics,
    Marketplace,
    PersonalArea,
    PersonalAreaVariable,
    SystemSettingConfig,
    SystemVariable,
    Warehouse,
)
from core.admin import (
    ReadOnlyModelAdmin,
)


@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'url',
        'currency',
        'type',
        'logistics',
    )


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(ExchangeRate)
class ExchangeRateAdmin(ReadOnlyModelAdmin):
    list_display = (
        'source',
        'destination',
        'rate',
        'rate_datetime',
    )


@admin.register(SystemSettingConfig)
class SystemSettingConfigAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'is_selected',
    )
    list_editable = (
        'is_selected',
    )
    filter_horizontal = (
        'system_variables',
    )


@admin.register(CategoryMatching)
class CategoryMatchingAdmin(admin.ModelAdmin):
    list_display = (
        'provider_category',
        'recipient_category',
    )
    readonly_fields = (
        'provider_category',
        'characteristic_mathing_button',
    )
    list_editable = (
        'recipient_category',
    )
    search_fields = (
        'provider_category__name',
        'provider_category__translated_name',
        'recipient_category__name',
    )
    autocomplete_fields = (
        'recipient_category',
    )
    fields = (
        'provider_category',
        'recipient_category',
        'characteristic_mathing_button',
    )

    list_per_page = 10

    def characteristic_mathing_button(self, matching):
        if matching.recipient_category:
            if not matching.characteristic_matchings.exists():
                result = format_html('Характеристики для категории пока не загружены')
            else:
                url = reverse('admin:common_characteristicmatching_changelist') + f'?category_matching_id={matching.id}'
                result = format_html(f'<a href="{url}" class="button" target="_blank">Сопоставить характеристики</a>')
        else:
            result = format_html('Для сопоставления характеристик необходимо сопоставить категорию')

        return result

    characteristic_mathing_button.short_description = ''


@admin.register(CharacteristicMatching)
class CharacteristicMatchingAdmin(admin.ModelAdmin):
    list_display = (
        'recipient_characteristic',
        'recipient_value',
        'is_raw',
        'value',
    )
    list_editable = (
        'value',
        'recipient_value',
    )
    autocomplete_fields = (
        'provider_characteristic',
        'recipient_value',
    )
    list_filter = (
        'recipient_characteristic__is_required',
    )
    fields = (
        'recipient_characteristic',
        'values_mathing_button',
        'value',
    )
    readonly_fields = (
        'values_mathing_button',
        'recipient_characteristic',
        'is_raw',
    )
    search_fields = (
        'recipient_characteristic__name',
    )

    list_per_page = 10

    def values_mathing_button(self, mathing):
        if mathing.recipient_characteristic.characteristic.has_reference_values:
            url = (
                    reverse('admin:common_characteristicvaluematching_changelist')
                    + f'?characteristic_matching_id={mathing.id}'
            )
            result = format_html(f'<a href="{url}" class="button" target="_blank">Сопоставить значения</a>')
        else:
            result = format_html('')

        return result

    values_mathing_button.short_description = ''

    def is_raw(self, mathing):
        return not mathing.recipient_characteristic.characteristic.has_reference_values

    is_raw.short_description = 'Является "сырым" значением'
    is_raw.boolean = True


@admin.register(CharacteristicValueMatching)
class CharacteristicValueMatchingAdmin(admin.ModelAdmin):
    list_display = (
        'recipient_characteristic_value',
        'provider_characteristic_value',
    )
    list_editable = (
        'provider_characteristic_value',
    )
    autocomplete_fields = (
        'provider_characteristic_value',
    )
    search_fields = (
        'recipient_characteristic_value__value',
    )
    readonly_fields = (
        'recipient_characteristic_value',
    )
    fields = (
        'recipient_characteristic_value',
        'provider_characteristic_value',
    )


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        'service_name',
        'entry',
        'timestamp',
    )
    list_filter = (
        'service_name',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.order_by(
            '-timestamp',
        )


@admin.register(SystemVariable)
class SystemVariableAdmin(admin.ModelAdmin):
    list_display = (
        'key',
        'value',
    )
    list_editable = (
        'value',
    )


@admin.register(Logistics)
class LogisticsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cost',
        'currency',
    )
    list_editable = (
        'cost',
        'currency',
    )


class PersonalAreaVariableAdmin(admin.TabularInline):
    model = PersonalAreaVariable
    extra = 0


class WarehouseInlineAdmin(admin.TabularInline):
    model = Warehouse
    extra = 0
    fields = (
        'name',
        'external_id',
    )


@admin.register(PersonalArea)
class PersonalAreaAdmin(admin.ModelAdmin):
    inlines = (
        PersonalAreaVariableAdmin,
        WarehouseInlineAdmin,
    )


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
        'personal_area__name',
    )
