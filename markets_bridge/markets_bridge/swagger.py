from django.conf import (
    settings,
)
from django.urls import (
    path,
)
from drf_yasg import (
    openapi,
)
from drf_yasg.views import (
    get_schema_view,
)
from rest_framework import (
    permissions,
)


contact = None

if settings.DEVELOPER_CONTACT_URL or settings.DEVELOPER_CONTACT_NAME:
    contact_kwargs = {}

    if settings.DEVELOPER_CONTACT_URL:
        contact_kwargs['url'] = settings.DEVELOPER_CONTACT_URL

    if settings.DEVELOPER_CONTACT_NAME:
        contact_kwargs['name'] = settings.DEVELOPER_CONTACT_NAME

    contact = openapi.Contact(**contact_kwargs)


schema_view_info = openapi.Info(
    title="Markets-Bridge API Doc.",
    default_version='v1',
)

if contact:
    schema_view_info.contact = contact

schema_view = get_schema_view(
    schema_view_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = (
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
)
