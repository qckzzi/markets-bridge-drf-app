from django.urls import (
    include,
    path,
)
from rest_framework.routers import (
    DefaultRouter,
)

from common.views import (
    CharacteristicMatchingAPIViewSet,
    LogsAPIViewSet,
    SystemVariablesAPIViewSet,
)


router = DefaultRouter()
router.register(
    r'system_variables',
    SystemVariablesAPIViewSet,
)
router.register(
    r'logs',
    LogsAPIViewSet,
    basename='log',
)
router.register(
    r'characteristic_matchings',
    CharacteristicMatchingAPIViewSet,
    basename='characteristic_matching',
)

urlpatterns = [
    path('', include(router.urls)),
]

