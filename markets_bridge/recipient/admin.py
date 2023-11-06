from django.contrib import (
    admin,
)

from recipient.models import (
    Category,
    Characteristic,
    CharacteristicValue,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name', 'parent_category')
    search_fields = ('external_id', 'name')
    readonly_fields = ('parent_category',)


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name', 'is_required', 'categories_name')
    search_fields = ('external_id', 'name', 'is_required', 'categories__name')
    readonly_fields = ('categories',)
    list_filter = ('is_required',)

    def categories_name(self, characteristic):
        return ', '.join(characteristic.categories.values_list('name', flat=True))

    categories_name.short_description = 'Категории'


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'characteristic', 'value')
    search_fields = ('external_id', 'characteristic__name', 'value')
