from django.conf import (
    settings,
)
from django.conf.urls.static import (
    static,
)
from django.contrib import (
    admin,
)
from django.urls import (
    include,
    path,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/parser_targets/', include('parser_targets.urls')),
    path('api/v1/common/', include('common.urls')),
    path('api/v1/provider/', include('provider.urls', 'provider')),
    path('api/v1/recipient/', include('recipient.urls', 'recipient')),
]

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

