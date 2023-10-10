from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from parser_targets.views import RawProductAPI, RawCategoryAPI
from provider.views import ScrappedProductAPI

router = DefaultRouter()
router.register(r'target_categories', RawCategoryAPI)
router.register(r'target_products', RawProductAPI)
router.register(r'products', ScrappedProductAPI)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
