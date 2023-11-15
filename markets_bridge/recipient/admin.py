from django.contrib import (
    admin,
)

from core.admin import (
    ReadOnlyModelAdmin,
)
from recipient.models import (
    Category,
    Characteristic,
    CharacteristicForCategory,
    CharacteristicValue,
)


@admin.register(Category)
class CategoryAdmin(ReadOnlyModelAdmin):
    list_display = (
        'external_id',
        'name',
        'parent_category',
    )
    search_fields = (
        'external_id',
        'name',
    )
    readonly_fields = (
        'parent_category',
    )


@admin.register(Characteristic)
class CharacteristicAdmin(ReadOnlyModelAdmin):
    list_display = (
        'external_id',
        'name',
    )
    search_fields = (
        'external_id',
        'name',
    )


@admin.register(CharacteristicForCategory)
class CharacteristicForCategoryAdmin(ReadOnlyModelAdmin):
    list_display = ('characteristic', 'category')
    search_fields = ('characteristic__name', 'category__name')


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(ReadOnlyModelAdmin):
    list_display = (
        'external_id',
        'characteristic',
        'value',
    )
    search_fields = (
        'external_id',
        'characteristic__name',
        'value',
    )
