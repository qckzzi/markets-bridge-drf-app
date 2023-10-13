from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import (
    GenericViewSet,
)

from provider.mixins import (
    OnlyExternalIdMixin,
)


class ProviderViewSet(
    OnlyExternalIdMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    pass
