from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from parser_targets.serializers import (
    RawCategorySerializer,
    RawProductSerializer,
)
from parser_targets.services import (
    get_allowed_categories,
    get_allowed_products,
)


class RawCategoryAPIViewSet(ReadOnlyModelViewSet):
    queryset = get_allowed_categories()
    serializer_class = RawCategorySerializer


class RawProductAPIViewSet(ReadOnlyModelViewSet):
    queryset = get_allowed_products()
    serializer_class = RawProductSerializer
