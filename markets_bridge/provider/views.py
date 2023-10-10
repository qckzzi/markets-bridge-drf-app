from rest_framework.viewsets import ModelViewSet

from provider.models import ScrappedProduct
from provider.serializer import ScrappedProductSerializer


class ScrappedProductAPI(ModelViewSet):
    queryset = ScrappedProduct.objects.all()
    serializer_class = ScrappedProductSerializer
