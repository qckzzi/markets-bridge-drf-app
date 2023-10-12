from django.contrib import (
    admin,
)

from provider.models import (
    ProductImage,
    ProviderCategory,
    ProviderCharacteristic,
    ProviderCharacteristicValue,
    ProviderMarketplace,
    ScrappedProduct,
)


@admin.register(ProviderMarketplace)
class ProviderMarketplaceAdmin(admin.ModelAdmin):
    pass


@admin.register(ProviderCategory)
class ProviderCategoryAdmin(admin.ModelAdmin):
    search_fields = ('external_id', 'name')


@admin.register(ProviderCharacteristic)
class ProviderCharacteristicAdmin(admin.ModelAdmin):
    pass


@admin.register(ProviderCharacteristicValue)
class ProviderCharacteristicValueAdmin(admin.ModelAdmin):
    pass


@admin.register(ScrappedProduct)
class ScrappedProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
