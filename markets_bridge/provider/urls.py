from django.urls import (
    include,
    path,
)
from rest_framework.routers import (
    DefaultRouter,
)

from provider.views import (
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

urlpatterns = [
    path('', include(router.urls)),
]
