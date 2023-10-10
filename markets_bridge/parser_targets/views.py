
from rest_framework.viewsets import ModelViewSet

from parser_targets.models import RawCategory, RawProduct
from parser_targets.serializers import RawCategorySerializer, RawProductSerializer


class RawCategoryAPI(ModelViewSet):
    queryset = RawCategory.objects.all()
    serializer_class = RawCategorySerializer


class RawProductAPI(ModelViewSet):
    queryset = RawProduct.objects.all()
    serializer_class = RawProductSerializer
