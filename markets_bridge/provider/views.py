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
    ProviderCharacteristic,
    ProviderCharacteristicValue,
    ScrappedProduct,
)
from provider.serializer import (
    ProductImageSerializer,
    ProviderCategorySerializer,
    ProviderCharacteristicSerializer,
    ProviderCharacteristicValueSerializer,
    ScrappedProductSerializer,
)


class ScrappedProductAPIViewSet(ModelViewSet):
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


class ProductImageAPIViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProviderCategoryAPIViewSet(ModelViewSet):
    serializer_class = ProviderCategorySerializer
    queryset = ProviderCategory.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProviderCharacteristicAPIViewSet(ModelViewSet):
    serializer_class = ProviderCharacteristicSerializer
    queryset = ProviderCharacteristic.objects.all()

    def create(self, request, *args, **kwargs):
        for char_number, record in enumerate(request.data):
            external_category_ids = record.get('provider_category')
            existing_category_ids = []

            try:
                for external_id in external_category_ids:
                    provider_category = ProviderCategory.objects.get(
                        external_id=external_id,
                    )
                    existing_category_ids.append(provider_category.id)
            except ProviderCategory.DoesNotExist:
                return Response(
                    {'error': 'Категория не найдена'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except ProviderCategory.MultipleObjectsReturned:
                return Response(
                    {'error': 'Найдено несколько категорий с указанным external_id'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request.data[char_number]['provider_category'] = existing_category_ids

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProviderCharacteristicValueAPIViewSet(ModelViewSet):
    serializer_class = ProviderCharacteristicValueSerializer
    queryset = ProviderCharacteristicValue.objects.all()

    def create(self, request, *args, **kwargs):
        for char_value_number, record in enumerate(request.data):
            external_characteristic_id = record.get('provider_characteristic')

            try:
                provider_characteristic = ProviderCharacteristic.objects.get(
                    external_id=external_characteristic_id,
                )
                existing_characteristic_id = provider_characteristic.id
            except ProviderCharacteristic.DoesNotExist:
                return Response(
                    {'error': 'Характеристика не найдена'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ProviderCharacteristic.DoesNotExist:
                return Response(
                    {'error': 'Найдено несколько характеристик с указанным external_id'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            request.data[char_value_number]['provider_characteristic'] =  existing_characteristic_id

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

