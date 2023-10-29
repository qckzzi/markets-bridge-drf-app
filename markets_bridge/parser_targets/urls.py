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


app_name = 'parser_targets'

router = DefaultRouter()
router.register(
    r'categories',
    RawCategoryAPI,
)
router.register(
    r'products',
    RawProductAPI,
)

urlpatterns = [
    path('', include(router.urls)),
]

