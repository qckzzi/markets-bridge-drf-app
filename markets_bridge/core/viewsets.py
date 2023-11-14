from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import (
    GenericViewSet,
)


class RetrieveViewSet(GenericViewSet, RetrieveModelMixin):
    pass


class CreateViewSet(GenericViewSet, CreateModelMixin):
    pass