from django.contrib import (
    admin,
)
from django.urls import (
    include,
    path,
)
from rest_framework.routers import (
    DefaultRouter,
)

from parser_targets.views import (
    RawCategoryAPI,
    RawProductAPI,
)
from provider.views import (
    ProductImageAPIViewSet,
    ProviderCategoryAPIViewSet,
    ProviderCharacteristicAPIViewSet,
    ProviderCharacteristicValueAPIViewSet,
    ScrappedProductAPIViewSet,
)
from recipient.views import (
    RecipientCategoryAPIViewSet,
    RecipientCharacteristicAPIViewSet,
    RecipientCharacteristicValueAPIViewSet,
    RecipientProductTypeAPIViewSet,
)


router = DefaultRouter()
router.register(
    r'target_categories',
    RawCategoryAPI,
)
router.register(
    r'target_products',
    RawProductAPI,
)
router.register(
    r'scrapped_products',
    ScrappedProductAPIViewSet,
)
router.register(
    r'product_images',
    ProductImageAPIViewSet,
)
router.register(
    r'provider_categories',
    ProviderCategoryAPIViewSet,
)
router.register(
    r'provider_characteristics',
    ProviderCharacteristicAPIViewSet,
)
router.register(
    r'provider_characteristic_values',
    ProviderCharacteristicValueAPIViewSet,
)
router.register(
    r'recipient_categories',
    RecipientCategoryAPIViewSet,
)
router.register(
    r'recipient_characteristics',
    RecipientCharacteristicAPIViewSet,
)
router.register(
    r'recipient_characteristic_values',
    RecipientCharacteristicValueAPIViewSet,
)
router.register(
    r'recipient_product_types',
    RecipientProductTypeAPIViewSet,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
