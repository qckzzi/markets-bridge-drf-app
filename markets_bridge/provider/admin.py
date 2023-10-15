from django.contrib import (
    admin,
)
from django.utils.html import (
    mark_safe,
)

from provider.models import (
    ProductCharacteristicValue,
    ProductImage,
    ProviderCategory,
    ProviderCharacteristic,
    ProviderCharacteristicValue,
    ProviderMarketplace,
    ScrappedProduct,
)


@admin.register(ProviderMarketplace)
class ProviderMarketplaceAdmin(admin.ModelAdmin):
    pass


@admin.register(ProviderCategory)
class ProviderCategoryAdmin(admin.ModelAdmin):
    search_fields = ('external_id', 'id', 'name', 'provider_marketplace__name')
    list_display = ('id', 'external_id', 'name', 'translated_name', 'recipient_category', 'provider_marketplace')
    raw_id_fields = ('recipient_category',)


@admin.register(ProviderCharacteristic)
class ProviderCharacteristicAdmin(admin.ModelAdmin):
    filter_horizontal = ('provider_category',)
    list_display = (
        'id', 
        'external_id', 
        'name', 
        'translated_name', 
        'related_category',
    )

    def related_category(self, obj):
        return [f'{category[0]} ({category[1]})' for category in obj.provider_category.values_list('name', 'translated_name')]

    related_category.short_description = 'Категории'

@admin.register(ProviderCharacteristicValue)
class ProviderCharacteristicValueAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'external_id', 
        'value', 
        'translated_value', 
        'provider_characteristic',
    )
    search_fields = ('external_id',)


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('image_preview',)
    extra = 0

    def image_preview(self, obj):
        return mark_safe(f'<img src = "{obj.image.url}" width = "300"/>')

    image_preview.short_description = ''
    image_preview.allow_tags = True


class ProductCharacteristicValueAdmin(admin.TabularInline):
    model = ProductCharacteristicValue
    raw_id_fields = ('provider_characteristic_value',)
    fields = ('provider_characteristic', 'provider_characteristic_value')
    readonly_fields = ('provider_characteristic',)
    extra = 0

    def provider_characteristic(self, product_char_value):
        return product_char_value.provider_characteristic_value.provider_characteristic.name_and_translate
    
    provider_characteristic.short_description = 'Характеристика'

@admin.register(ScrappedProduct)
class ScrappedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'translated_name', 'price', 'currency', 'provider_category', 'status', 'marketplace')
    readonly_fields = ('currency', 'import_date', 'update_date', 'upload_date', 'external_id')
    fields = (
        ('name', 'translated_name'),
        ('price', 'currency'),
        ('description', 'translated_description'),
        'import_date', 
        'update_date', 
        'upload_date',
        'status',
        'provider_category',
        'external_id',
    )
    list_editable = ('status',)
    inlines = (ProductImageAdmin, ProductCharacteristicValueAdmin)

    def currency(self, product):
        return product.provider_category.provider_marketplace.currency.name
    
    currency.short_description = 'Валюта'

    def marketplace(self, product):
        return product.provider_category.provider_marketplace.name

    marketplace.short_description = 'Поставщик'

