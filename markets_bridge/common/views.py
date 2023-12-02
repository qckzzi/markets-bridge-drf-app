from rest_framework import (
    status,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    GenericViewSet,
)
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)

from common.serializers import (
    LogSerializer,
    SystemVariableSerializer,
)
from common.services import (
    create_characteristic_matchings_by_category_matching_id,
    get_system_variables,
)
from core.viewsets import (
    CreateViewSet,
    RetrieveViewSet,
)


class SystemVariablesAPIViewSet(RetrieveViewSet):
    queryset = get_system_variables()
    serializer_class = SystemVariableSerializer
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
        category_matching_id = request.data['category_matching_id']
        create_characteristic_matchings_by_category_matching_id(category_matching_id)

        return Response(status=status.HTTP_201_CREATED)
