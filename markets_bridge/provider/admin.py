from decimal import (
    Decimal,
)

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
from django_admin_listfilter_dropdown.filters import (
    RelatedOnlyDropdownFilter,
)
from rest_framework.reverse import (
    reverse,
)

from common.models import (
    Warehouse,
)
from core.admin import (
    BaseNullFilter,
    BaseYesOrNoFilter,
)
from provider.enums import (
    ProductStatusEnum,
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
from provider.services import (
    compare_product_characteristics,
    update_product_export_allowance,
    update_products_status,
)
from provider.strings import (
    ARCHIVE_PRODUCT_IS_SUCCESS,
    BLANK_VALUE_FOR_UPDATE_MESSAGE,
    COMPARE_PRODUCT_CHARACTERISTICS_IS_SUCCESS,
    LOAD_PRODUCT_IS_SUCCESS,
    UPDATE_PRODUCT_IS_SUCCESS,
)
from provider.utils import (
    archive_products,
    load_product,
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
    autocomplete_fields = (
        'recipient_characteristic_values',
    )


class ProductValueAdmin(admin.TabularInline):
    readonly_fields = (
        'characteristic',
        'value',
        'recipient_characteristic_values',
    )
    model = ProductValue
    extra = 0

    def characteristic(self, product_value):
        return product_value.value.characteristic

    characteristic.short_description = 'Характеристика'

    def recipient_characteristic_values(self, product_value):
        return ', '.join(
            product_value.value.recipient_characteristic_values.values_list(
                'value',
                flat=True,
            )
        ) or 'Не сопоставлено'

    recipient_characteristic_values.short_description = 'Значения характеристики с системе получателя'


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
    markup = forms.IntegerField(
        min_value=0,
        label='Коэффициент наценки, %',
        required=False,
    )
    width = forms.DecimalField(
        min_value=0,
        label='Ширина, см',
        required=False,
    )
    height = forms.DecimalField(
        min_value=0,
        label='Высота, см',
        required=False,
    )
    depth = forms.DecimalField(
        min_value=0,
        label='Глубина, см',
        required=False,
    )
    weight = forms.DecimalField(
        min_value=0,
        label='Вес товара, кг',
        required=False,
    )


class IsMatchedCategoryFilter(BaseYesOrNoFilter):
    title = 'Сопоставлена ли категория?'
    parameter_name = 'is_matched_category'

    def queryset(self, request, queryset):
        value = self.value()

        if value is not None:
            is_not_matched = value == 'False'
            queryset = queryset.filter(
                category__matching__recipient_category__isnull=is_not_matched,
            )

        return queryset


class AvailableFilter(BaseYesOrNoFilter):
    title = 'В наличии'
    parameter_name = 'available'

    def queryset(self, request, queryset):
        value = self.value()

        if value is not None:
            is_available = value == 'True'

            if is_available:
                queryset = queryset.filter(
                    stock_quantity__gt=0,
                )
            else:
                queryset = queryset.filter(
                    stock_quantity=0,
                )

        return queryset


class BaseDimensionsBlankFilter(BaseYesOrNoFilter):
    dimension_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.blank_filter_kwargs = {f'{self.dimension_name}': Decimal('0.00')}
        self.not_blank_filter_kwargs = {f'{self.dimension_name}__gt': Decimal('0.00')}

    def queryset(self, request, queryset):
        value = self.value()

        if value is not None:
            value_is_blank = value == 'True'
            filter_kwargs = self.blank_filter_kwargs if value_is_blank else self.not_blank_filter_kwargs
            queryset = queryset.filter(
                **filter_kwargs,
            )

        return queryset

class WidthIsBlankFilter(BaseDimensionsBlankFilter):
    dimension_name = 'width'
    title = 'Пустая ширина'
    parameter_name = 'width_is_blank'


class HeightIsBlankFilter(BaseDimensionsBlankFilter):
    dimension_name = 'height'
    title = 'Пустая высота'
    parameter_name = 'height_is_blank'


class DepthIsBlankFilter(BaseDimensionsBlankFilter):
    dimension_name = 'depth'
    title = 'Пустая глубина'
    parameter_name = 'depth_is_blank'


class WeightIsBlankFilter(BaseDimensionsBlankFilter):
    dimension_name = 'weight'
    title = 'Пустой вес'
    parameter_name = 'weight_is_blank'


class WarehouseIsNullFilter(BaseNullFilter):
    field_name = 'warehouse'
    title = 'Отсутствует склад'
    parameter_name = 'warehouse_is_null'


class ArchivedFilter(BaseYesOrNoFilter):
    title = 'В архиве'
    parameter_name = 'is_archived'
    default_value = 'False'

    def queryset(self, request, queryset):
        value = self.value()

        if value is not None:
            is_archived = value == 'True'

            if is_archived:
                queryset = queryset.filter(
                    status=ProductStatusEnum.ARCHIVED,
                )
            else:
                queryset = queryset.filter(
                    status=ProductStatusEnum.ACTIVE,
                )

        return queryset

    def value(self):
        value = super().value()

        if value is None:
            value = self.default_value

        return value

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
            }


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class DiscountedPriceFromFilter(InputFilter):
    parameter_name = 'discounted_price_from'
    title = 'Цена со скидкой от'

    def queryset(self, request, queryset):
        if self.value() is not None:
            price = self.value()
            return queryset.filter(
                discounted_price__gte=price,
            )


class DiscountedPriceTOFilter(InputFilter):
    parameter_name = 'discounted_price_to'
    title = 'Цена со скидкой до'

    def queryset(self, request, queryset):
        if self.value() is not None:
            price = self.value()
            return queryset.filter(
                discounted_price__lte=price,
            )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'vendor_code',
        'preview_image',
        'brand',
        'name',
        'translated_name',
        'discounted_price',
        'currency',
        'category',
        'is_export_allowed',
        'marketplace',
        'stock_quantity',
    )
    list_display_links = (
        'vendor_code',
        'preview_image',
    )
    search_fields = (
        'id',
        'name',
        'translated_name',
        'category__name',
    )
    readonly_fields = (
        'vendor_code',
        'brand',
        'currency',
        'import_date',
        'update_date',
        'upload_date',
        'external_id',
        'characteristic_values',
        'category',
        'category_mathing_button',
    )
    fields = (
        ('vendor_code', 'external_id'),
        ('product_code', 'name', 'translated_name'),
        ('description', 'translated_description'),
        'brand',
        'url',
        ('price', 'discounted_price', 'currency', 'markup'),
        ('warehouse', 'stock_quantity'),
        ('width', 'height', 'depth', 'weight'),
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
        DiscountedPriceFromFilter,
        DiscountedPriceTOFilter,
        'is_export_allowed',
        IsMatchedCategoryFilter,
        ('category', RelatedOnlyDropdownFilter),
        ('brand', RelatedOnlyDropdownFilter),
        ('marketplace', RelatedOnlyDropdownFilter),
        WarehouseIsNullFilter,
        WidthIsBlankFilter,
        HeightIsBlankFilter,
        DepthIsBlankFilter,
        WeightIsBlankFilter,
        AvailableFilter,
        ArchivedFilter,
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
        'allow_export',
        'disallow_export',
        'update_markup',
        'update_width',
        'update_height',
        'update_depth',
        'update_weight',
        'archive',
        'return_from_archive',
        'compare_product_characteristics',
        'load_product',
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

    def allow_export(self, request, queryset):
        update_product_export_allowance(queryset, is_allowed=True)
        messages.success(request, 'Товары успешно обновлены!')

    allow_export.short_description = 'Разрешить экспорт'

    def disallow_export(self, request, queryset):
        update_product_export_allowance(queryset, is_allowed=False)
        messages.success(request, 'Товары успешно обновлены!')

    disallow_export.short_description = 'Запретить экспорт'

    def update_markup(self, request, queryset):
        form = self.action_form(request.POST)
        form.full_clean()
        markup = form.cleaned_data['markup']

        if not markup:
            messages.error(request, 'Пожалуйста, укажите наценку для обновления товаров.')
            return

        queryset.update(
            markup=markup,
        )
        messages.success(request, f'Наценка в {markup}% успешно обновлена у товаров!')

    update_markup.short_description = 'Изменить наценку'

    def update_width(self, request, queryset):
        self._update_value(request, queryset, 'width')

    update_width.short_description = 'Изменить ширину'

    def update_height(self, request, queryset):
        self._update_value(request, queryset, 'height')

    update_height.short_description = 'Изменить высоту'

    def update_depth(self, request, queryset):
        self._update_value(request, queryset, 'depth')

    update_depth.short_description = 'Изменить глубину'

    def update_weight(self, request, queryset):
        self._update_value(request, queryset, 'weight')

    update_weight.short_description = 'Изменить вес'

    def archive(self, request, queryset):
        archive_products(queryset)
        update_products_status(queryset, ProductStatusEnum.ARCHIVED)
        messages.success(request, ARCHIVE_PRODUCT_IS_SUCCESS)

    archive.short_description = 'Архивировать'

    def compare_product_characteristics(self, request, queryset):
        for product in queryset:
            compare_product_characteristics(product.id)
        
        messages.success(request, COMPARE_PRODUCT_CHARACTERISTICS_IS_SUCCESS)
    
    compare_product_characteristics.short_description = 'Сопоставить данные товаров с получателем'
    
    def load_product(self, request, queryset):
        for product in queryset:
            if product.warehouse:
                load_product(product.id)
        
        messages.success(request, LOAD_PRODUCT_IS_SUCCESS)
    
    load_product.short_description = 'Выгрузить товары'

    def return_from_archive(self, request, queryset):
        update_products_status(queryset, ProductStatusEnum.ACTIVE)
        messages.success(request, UPDATE_PRODUCT_IS_SUCCESS)

    return_from_archive.short_description = 'Вернуть из архива'

    def _update_value(self, request, queryset, field_name):
        form = self.action_form(request.POST)
        form.full_clean()
        value = form.cleaned_data[field_name]

        if not value:
            messages.error(request, BLANK_VALUE_FOR_UPDATE_MESSAGE)
            return

        queryset.update(
            **{field_name:value},
        )
        messages.success(request, UPDATE_PRODUCT_IS_SUCCESS)

    def currency(self, product):
        if product.category:
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

        if recipient_category := product.category.matching.recipient_category:
            result = format_html(f'Категория товара сопоставлена с категорией получателя "{recipient_category.name}".<br><br><a href="{url}" class="button" target="_blank">Посмотреть сопоставление</a>')
        else:
            result = format_html(f'<a href="{url}" class="button" target="_blank">Сопоставить категорию</a>')

        return result

    category_mathing_button.short_description = ''

    def vendor_code(self, product):
        return product.vendor_code

    vendor_code.short_description = 'Артикул'


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
