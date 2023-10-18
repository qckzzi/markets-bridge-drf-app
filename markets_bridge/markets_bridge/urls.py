from django.conf import (
    settings,
)
from django.conf.urls.static import (
    static,
)
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
    ProductCharacteristicValueAPIViewSet,
    ProductImageAPIViewSet,
    ProviderCategoryAPIViewSet,
    ProviderCharacteristicAPIViewSet,
    ProviderCharacteristicValueAPIViewSet,
    ScrappedProductAPIViewSet,
)
from recipient.views import (
    MatchingRecipientCategoriesAPIView,
    RecipientCategoryAPIViewSet,
    RecipientCharacteristicAPIViewSet,
    RecipientCharacteristicValueAPIViewSet,
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
    r'provider_product_characteristic_values',
    ProductCharacteristicValueAPIViewSet,
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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/mathing_recipient_categories/', MatchingRecipientCategoriesAPIView.as_view()),
]

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

