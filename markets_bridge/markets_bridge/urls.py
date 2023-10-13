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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
