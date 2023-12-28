from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)


class ReadOnlyAdminMixin:
    """ReadOnly дополнение к классу ModelAdmin."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AuthenticationMixin:
    """Дополнение к ViewSet с типичной аутентификацией для проекта."""

    authentication_classes = (JWTAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)