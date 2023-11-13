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
    create_or_update_product,
    get_or_create_brand,
    get_or_create_category,
    get_or_create_characteristic_value,
    update_or_create_characteristic,
)


class ProductAPIViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        product, is_new = create_or_update_product(request.data)
        serializer = self.get_serializer(product)

        if is_new:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_200_OK

        return Response(status=http_status, data=serializer.data)


class ProductImageAPIViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class CategoryAPIViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    def create(self, request, *args, **kwargs):
        category, is_new = get_or_create_category(request.data)

        if is_new:
            serializer = self.get_serializer(category)
            response = Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            response = Response(
                data={'message': f'The "{category.name}" category already exists.'},
                status=status.HTTP_200_OK,
            )

        return response


class CharacteristicAPIViewSet(ModelViewSet):
    serializer_class = CharacteristicSerializer
    queryset = Characteristic.objects.all()

    def create(self, request, *args, **kwargs):
        characteristic, is_new = update_or_create_characteristic(request.data)

        if is_new:
            serializer = self.get_serializer(characteristic)
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(
                data={'message': f'The "{characteristic.name}" characteristic already exists.'},
                status=status.HTTP_200_OK,
            )

        return response


class CharacteristicValueAPIViewSet(ModelViewSet):
    serializer_class = CharacteristicValueSerializer
    queryset = CharacteristicValue.objects.all()

    def create(self, request, *args, **kwargs):
        characteristic_value, is_new = get_or_create_characteristic_value(request.data)

        if is_new:
            serializer = self.get_serializer(characteristic_value)
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(
                data={'message': f'The "{characteristic_value.value}" characteristic value already exists.'},
                status=status.HTTP_200_OK,
            )

        return response


class BrandAPIViewSet(ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

    def create(self, request, *args, **kwargs):
        brand, is_new = get_or_create_brand(request.data)
        serializer = self.get_serializer(brand)

        if is_new:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        return Response(data=serializer.data, status=status_code)
