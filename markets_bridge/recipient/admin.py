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

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)

        # FIXME: Бизнес-логика в UI ;(
        queryset = queryset.filter(
            parent_category__isnull=False,
        ).distinct()

        return queryset, may_have_duplicates


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
