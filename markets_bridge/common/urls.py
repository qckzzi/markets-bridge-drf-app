from django.urls import (
    include,
    path,
)
from rest_framework.routers import (
    DefaultRouter,
)

from common.views import (
    LogsAPIViewSet,
    SystemEnvironmentsAPIViewSet,
)


router = DefaultRouter()
router.register(
    r'system_environments',
    SystemEnvironmentsAPIViewSet,
)
router.register(
    r'logs',
    LogsAPIViewSet,
    basename='log',
)

urlpatterns = [
    path('', include(router.urls)),
]

