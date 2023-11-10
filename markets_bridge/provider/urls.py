from django.urls import (
    include,
    path,
)
from rest_framework.routers import (
    DefaultRouter,
)

from provider.views import (
    BrandAPIViewSet,
    CategoryAPIViewSet,
    CharacteristicAPIViewSet,
    CharacteristicValueAPIViewSet,
    ProductAPIViewSet,
    ProductImageAPIViewSet,
)


app_name = 'provider'

router = DefaultRouter()
router.register(
    r'products',
    ProductAPIViewSet,
)
router.register(
    r'product_images',
    ProductImageAPIViewSet,
)
router.register(
    r'categories',
    CategoryAPIViewSet,
)
router.register(
    r'characteristics',
    CharacteristicAPIViewSet,
)
router.register(
    r'characteristic_values',
    CharacteristicValueAPIViewSet,
)
router.register(
    r'brands',
    BrandAPIViewSet,
)

urlpatterns = [
    path('', include(router.urls)),
]
