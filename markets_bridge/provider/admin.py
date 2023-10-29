from django.contrib import (
    admin,
)
from django.utils.html import (
    mark_safe,
)

from provider.models import (
    Category,
    Characteristic,
    CharacteristicValue,
    Product,
    ProductImage,
    ProductValue,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name', 'translated_name', 'recipient_category', 'marketplace')
    search_fields = ('external_id', 'name', 'translated_name',)
    raw_id_fields = ('recipient_category',)


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories',)
    list_display = ('external_id', 'name', 'translated_name', 'is_required')
    search_fields = ('external_id', 'name', 'translated_name')
    raw_id_fields = ('recipient_characteristic',)


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'value', 'translated_value', 'characteristic')
    search_fields = ('external_id', 'value', 'translated_value')
    raw_id_fields = ('recipient_characteristic_value',)


class ProductValueAdmin(admin.TabularInline):
    fields = ('value_characteristic', 'value')
    readonly_fields = fields
    model = ProductValue
    extra = 0

    def value_characteristic(self, product_value):
        return product_value.value.characteristic

    value_characteristic.short_description = 'Характеристика'


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('image_preview',)
    extra = 0

    def image_preview(self, obj):
        return mark_safe(f'<img src = "{obj.image.url}" width = "300"/>')

    image_preview.short_description = ''
    image_preview.allow_tags = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('preview_image', 'name', 'translated_name', 'price', 'currency', 'category', 'status', 'marketplace')
    search_fields = ('name', 'translated_name', 'description', 'translated_description', 'provider_category__name')
    readonly_fields = ('currency', 'import_date', 'update_date', 'upload_date', 'external_id', 'characteristic_values', 'url')
    fields = (
        'external_id',
        ('name', 'translated_name'),
        'url',
        ('price', 'discounted_price', 'currency'),
        'import_date', 
        'update_date', 
        'upload_date',
        'status',
        'category',
    )
    filter_horizontal = ('characteristic_values',)
    list_editable = ('status',)
    inlines = (ProductImageAdmin, ProductValueAdmin)

    def currency(self, product):
        return product.category.marketplace.currency.name
    
    currency.short_description = 'Валюта'

    def marketplace(self, product):
        return product.category.marketplace.name

    marketplace.short_description = 'Поставщик'

    def preview_image(self, product):
        return mark_safe(f'<img src = "{product.images.first().image.url}" width="100"/>')

    preview_image.short_description = 'Изображение'

