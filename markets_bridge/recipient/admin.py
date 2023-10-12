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
    pass


@admin.register(RecipientCharacteristic)
class RecipientCharacteristicAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipientCharacteristicValue)
class RecipientCharacteristicValueAdmin(admin.ModelAdmin):
    pass
