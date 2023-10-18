from django.contrib import (
    admin,
)

from recipient.models import (
    RecipientCategory,
    RecipientCharacteristic,
    RecipientCharacteristicValue,
    RecipientMarketplace,
)


@admin.register(RecipientMarketplace)
class RecipientMarketplaceAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipientCategory)
class RecipientCategoryAdmin(admin.ModelAdmin):
    search_fields = ('external_id', 'id')
    list_display = ('id', 'external_id', 'name', 'parent_categories')

    def parent_categories(self, obj):
        return ', '.join([category.name for category in obj.parent_categories.all()])

    parent_categories.short_description = 'Родительские категории'


@admin.register(RecipientCharacteristic)
class RecipientCharacteristicAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'is_required')


@admin.register(RecipientCharacteristicValue)
class RecipientCharacteristicValueAdmin(admin.ModelAdmin):
    pass
