from rest_framework import (
    status,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from common.serializers import (
    CharacteristicMatchingSerializer,
    LogSerializer,
    SystemVariableSerializer,
)
from common.services import (
    create_characteristic_matchings_by_category_matching_id,
    get_logs,
    get_system_variables,
)
from core.mixins import (
    AuthenticationMixin,
)


class SystemVariablesAPIViewSet(AuthenticationMixin, ReadOnlyModelViewSet):
    queryset = get_system_variables()
    serializer_class = SystemVariableSerializer
    lookup_field = 'key'


class LogsAPIViewSet(AuthenticationMixin, ModelViewSet):
    serializer_class = LogSerializer
    queryset = get_logs()


class CharacteristicMatchingAPIViewSet(AuthenticationMixin, GenericViewSet):
    serializer_class = CharacteristicMatchingSerializer

    @action(['POST'], detail=False)
    def create_by_category_matching(self, request):
        category_matching_id = request.data['category_matching_id']
        create_characteristic_matchings_by_category_matching_id(category_matching_id)

        return Response(status=status.HTTP_201_CREATED)
