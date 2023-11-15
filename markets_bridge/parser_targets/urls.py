from django.urls import (
    include,
    path,
)
from rest_framework.routers import (
    DefaultRouter,
)

from parser_targets.views import (
    RawCategoryAPIViewSet,
    RawProductAPIViewSet,
)


app_name = 'parser_targets'

router = DefaultRouter()
router.register(
    r'categories',
    RawCategoryAPIViewSet,
)
router.register(
    r'products',
    RawProductAPIViewSet,
)

urlpatterns = [
    path('', include(router.urls)),
]

