from rest_framework.decorators import (
    action,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.viewsets import (
    GenericViewSet,
)
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)

from common.serializers import (
    LogSerializer,
    SystemEnvironmentSerializer,
)
from common.services import (
    get_system_environments,
)
from core.viewsets import (
    CreateViewSet,
    RetrieveViewSet,
)


class SystemEnvironmentsAPIViewSet(RetrieveViewSet):
    queryset = get_system_environments()
    serializer_class = SystemEnvironmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class LogsAPIViewSet(CreateViewSet):
    serializer_class = LogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CharacteristicMatchingAPIViewSet(GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(['POST'], detail=False)
    def create_by_category_matching(self, request):
        ...
