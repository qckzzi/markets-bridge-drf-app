from django.contrib import (
    admin,
)

from recipient.models import (
    RecipientCategory,
    RecipientCharacteristic,
    RecipientCharacteristicValue,
    RecipientMarketplace,
    RecipientProductType,
)


@admin.register(RecipientMarketplace)
class RecipientMarketplaceAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipientCategory)
class RecipientCategoryAdmin(admin.ModelAdmin):
    search_fields = ('external_id', 'id')
    list_display = ('id', 'external_id', 'name', 'parent')


@admin.register(RecipientProductType)
class RecipientProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'related_category')
    search_fields = ('name',)

    def related_category(self, obj):
        return ', '.join([category.name for category in obj.category.all()])


@admin.register(RecipientCharacteristic)
class RecipientCharacteristicAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipientCharacteristicValue)
class RecipientCharacteristicValueAdmin(admin.ModelAdmin):
    pass
