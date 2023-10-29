from django.urls import (
    include,
    path,
)
from rest_framework.routers import (
    DefaultRouter,
)

from recipient.views import (
    CategoryAPIViewSet,
    CharacteristicAPIViewSet,
    CharacteristicValueAPIViewSet,
)


app_name = 'recipient'

router = DefaultRouter()
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
