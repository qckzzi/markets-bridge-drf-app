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
    list_display = ('external_id', 'name', 'parents')
    search_fields = ('external_id', 'name')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(children__isnull=True)

    def parents(self, category):
        return ', '.join(category.parent_categories.values_list('name', flat=True))

    parents.short_description = 'Родительские категории'


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name', 'is_required', 'categories_name')
    search_fields = ('external_id', 'name', 'is_required', 'categories__name')
    readonly_fields = ('categories',)

    def categories_name(self, characteristic):
        return ', '.join(characteristic.categories.values_list('name', flat=True))

    categories_name.short_description = 'Категории'


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'characteristic', 'value')
    search_fields = ('external_id', 'characteristic__name', 'value')
