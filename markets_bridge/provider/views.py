from rest_framework import (
    status,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    ModelViewSet,
)

from core.mixins import (
    AuthenticationMixin,
)
from provider.models import (
    Brand,
    Category,
    Characteristic,
    CharacteristicValue,
    Product,
    ProductImage,
)
from provider.serializer import (
    BrandSerializer,
    CategorySerializer,
    CharacteristicSerializer,
    CharacteristicValueSerializer,
    ProductImageSerializer,
    ProductSerializer,
)
from provider.services import (
    compare_product_characteristics,
    create_or_update_product,
    get_or_create_brand,
    get_or_create_category,
    get_or_create_characteristic_value,
    update_or_create_characteristic,
)
from rest_framework.decorators import (
    action,
)


class ProductAPIViewSet(AuthenticationMixin, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        product, is_new = create_or_update_product(request.data)

        if is_new:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_200_OK

        return Response(status=http_status, data={"id": product.id})
    
    @action(['POST'], detail=False)
    def compare_characteristics(self, request):
        product_id = request.data['product_id']
        compare_product_characteristics(product_id)

        return Response(status=status.HTTP_201_CREATED)

class ProductImageAPIViewSet(AuthenticationMixin, ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class CategoryAPIViewSet(AuthenticationMixin, ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    def create(self, request, *args, **kwargs):
        category, is_new = get_or_create_category(request.data)

        if is_new:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_200_OK

        return Response(status=http_status, data={"id": category.id})


class CharacteristicAPIViewSet(AuthenticationMixin, ModelViewSet):
    serializer_class = CharacteristicSerializer
    queryset = Characteristic.objects.all()

    def create(self, request, *args, **kwargs):
        characteristic, is_new = update_or_create_characteristic(request.data)

        if is_new:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_200_OK

        return Response(status=http_status, data={"id": characteristic.id})


class CharacteristicValueAPIViewSet(AuthenticationMixin, ModelViewSet):
    serializer_class = CharacteristicValueSerializer
    queryset = CharacteristicValue.objects.all()

    def create(self, request, *args, **kwargs):
        characteristic_value, is_new = get_or_create_characteristic_value(request.data)

        if is_new:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_200_OK

        return Response(status=http_status, data={"id": characteristic_value.id})


class BrandAPIViewSet(AuthenticationMixin, ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

    def create(self, request, *args, **kwargs):
        brand, is_new = get_or_create_brand(request.data)

        if is_new:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_200_OK

        return Response(status=http_status, data={"id": brand.id})
