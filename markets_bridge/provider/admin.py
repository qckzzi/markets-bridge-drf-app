from django.contrib import admin
from provider.models import (
    ProviderMarketplace,
    ProviderCategory,
    ProviderCharacteristic,
    ProviderCharacteristicValue,
    ScrappedProduct,
    ProductImage,
)


@admin.register(ProviderMarketplace)
class ProviderMarketplaceAdmin(admin.ModelAdmin):
    pass


@admin.register(ProviderCategory)
class ProviderCategoryAdmin(admin.ModelAdmin):
    pass


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
