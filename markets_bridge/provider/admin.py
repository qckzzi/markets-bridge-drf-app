from django import (
    forms,
)
from django.contrib import (
    admin,
    messages,
)
from django.contrib.admin.helpers import (
    ActionForm,
)
from django.utils.html import (
    format_html,
    mark_safe,
)
from rest_framework.reverse import (
    reverse,
)

from common.models import (
    Warehouse,
)
from provider.models import (
    Brand,
    Category,
    Characteristic,
    CharacteristicValue,
    Product,
    ProductImage,
    ProductValue,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'external_id',
        'name',
        'translated_name',
        'marketplace',
    )
    search_fields = (
        'external_id',
        'name',
        'translated_name',
    )
    readonly_fields = (
        'external_id',
        'name',
        'marketplace',
    )


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'categories',
    )
    list_display = (
        'external_id',
        'name',
        'translated_name',
    )
    search_fields = (
        'external_id',
        'name',
        'translated_name',
    )
    readonly_fields = (
        'external_id',
        'name',
        'marketplace',
        'categories',
    )


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    list_display = (
        'external_id',
        'value',
        'translated_value',
        'characteristic',
    )
    search_fields = (
        'external_id',
        'value',
        'translated_value',
    )
    readonly_fields = (
        'external_id',
        'value',
        'marketplace',
        'characteristic',
    )


class ProductValueAdmin(admin.TabularInline):
    readonly_fields = (
        'value_characteristic',
        'value',
    )
    model = ProductValue
    extra = 0

    def value_characteristic(self, product_value):
        return product_value.value.characteristic

    value_characteristic.short_description = 'Характеристика'


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    readonly_fields = (
        'image_preview',
    )
    extra = 0

    def image_preview(self, obj):
        return mark_safe(f'<img src = "{obj.image.url}" width = "300"/>')

    image_preview.short_description = ''
    image_preview.allow_tags = True


class ProductActionForm(ActionForm):
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        required=False,
        label='Склад',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'preview_image',
        'brand',
        'product_code',
        'name',
        'translated_name',
        'discounted_price',
        'currency',
        'category',
        'is_export_allowed',
        'marketplace',
    )
    list_display_links = (
        'id',
        'preview_image',
    )
    search_fields = (
        'id',
        'name',
        'translated_name',
        'category__name',
    )
    readonly_fields = (
        'brand',
        'currency',
        'import_date',
        'update_date',
        'upload_date',
        'external_id',
        'characteristic_values',
        'product_url',
        'category',
        'category_mathing_button',
    )
    fields = (
        'external_id',
        ('product_code', 'name', 'translated_name'),
        'brand',
        'product_url',
        ('price', 'discounted_price', 'currency', 'markup'),
        ('warehouse', 'stock_quantity', 'weight'),
        'import_date', 
        'update_date', 
        'upload_date',
        ('is_export_allowed', 'is_updated'),
        'category',
        'category_mathing_button',
    )
    filter_horizontal = (
        'characteristic_values',
    )
    list_editable = (
        'is_export_allowed',
    )
    list_filter = (
        'is_export_allowed',
    )
    autocomplete_fields = (
        'warehouse',
    )
    inlines = (
        ProductImageAdmin,
        ProductValueAdmin,
    )
    actions = (
        'change_warehouse',
    )
    action_form = ProductActionForm
    list_per_page = 25

    def change_warehouse(self, request, queryset):
        form = self.action_form(request.POST)
        form.full_clean()
        warehouse = form.cleaned_data['warehouse']

        if not warehouse:
            messages.error(request, 'Пожалуйста, укажите склад для обновления товаров.')
            return

        queryset.update(
            warehouse=warehouse,
        )
        messages.success(request, f'Склад {warehouse.name} успешно установлен для товаров.')

    change_warehouse.short_description = 'Изменить склад'

    def currency(self, product):
        return product.category.marketplace.currency.name
    
    currency.short_description = 'Валюта'

    def marketplace(self, product):
        return product.category.marketplace.name

    marketplace.short_description = 'Поставщик'

    def preview_image(self, product):
        if product.images.exists():
            return mark_safe(f'<img src = "{product.images.first().image.url}" width="100"/>')

    preview_image.short_description = 'Изображение'

    def category_mathing_button(self, product):
        category_id = product.category_id
        url = reverse('admin:common_categorymatching_changelist') + f'?provider_category_id={category_id}'

        return format_html(f'<a href="{url}" class="button" target="_blank">Сопоставить категорию</a>')

    category_mathing_button.short_description = ''

    def product_url(self, product):
        return format_html(f'<a href="{product.url}" target="_blank">{product.url}</a>')

    product_url.short_description = 'URL товара'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'external_id',
        'name',
        'marketplace',
    )
    readonly_fields = (
        'id',
        'marketplace',
    )
    search_fields = (
        'id',
        'external_id',
        'name',
    )
