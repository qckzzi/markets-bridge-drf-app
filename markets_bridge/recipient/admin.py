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
    list_display = ('external_id', 'name')
    search_fields = ('external_id', 'name')


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'characteristic', 'value')
    search_fields = ('external_id', 'characteristic__name', 'value')
