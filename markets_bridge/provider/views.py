from rest_framework import (
    status,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    ModelViewSet,
)

from provider.models import (
    ProductImage,
    ProviderCategory,
    ScrappedProduct,
)
from provider.serializer import (
    ProductImageSerializer,
    ScrappedProductSerializer,
)


class ScrappedProductAPI(ModelViewSet):
    queryset = ScrappedProduct.objects.all()
    serializer_class = ScrappedProductSerializer

    def create(self, request, *args, **kwargs):
        external_id = request.data.get('provider_category_external_id')

        try:
            provider_category = ProviderCategory.objects.get(external_id=external_id)
        except ProviderCategory.DoesNotExist:
            return Response(
                {'error': 'Категория не найдена'}, status=status.HTTP_400_BAD_REQUEST
            )

        request.data['provider_category'] = provider_category.id

        return super().create(request, *args, **kwargs)


class ProductImageAPI(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

