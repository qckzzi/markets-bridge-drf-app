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
    ProductImageAPI,
    ScrappedProductAPI,
)


router = DefaultRouter()
router.register(r'target_categories', RawCategoryAPI)
router.register(r'target_products', RawProductAPI)
router.register(r'scrapped_products', ScrappedProductAPI)
router.register(r'product_images', ProductImageAPI)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
