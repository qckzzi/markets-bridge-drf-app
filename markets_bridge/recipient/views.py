from rest_framework import (
    status,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    ModelViewSet,
)

from recipient.models import (
    RecipientCategory,
    RecipientCharacteristic,
    RecipientCharacteristicValue,
    RecipientProductType,
)
from recipient.serializers import (
    RecipientCategorySerializer,
    RecipientCharacteristicSerializer,
    RecipientCharacteristicValueSerializer,
    RecipientProductTypeSerializer,
)


class RecipientCategoryAPIViewSet(ModelViewSet):
    serializer_class = RecipientCategorySerializer
    queryset = RecipientCategory.objects.all()

    def create(self, request, *args, **kwargs):
        parent_external_id = request.data.get('parent')
        if parent_external_id:
            try:
                recipient_category = RecipientCategory.objects.get(
                    external_id=parent_external_id,
                )
            except RecipientCategory.DoesNotExist:
                return Response(
                    {'error': 'Категория не найдена'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except RecipientCategory.MultipleObjectsReturned:
                return Response(
                    {'error': 'Найдено несколько категорий с указанным external_id'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                request.data['parent'] = recipient_category.id

        return super().create(request, *args, **kwargs)


class RecipientProductTypeAPIViewSet(ModelViewSet):
    serializer_class = RecipientProductTypeSerializer
    queryset = RecipientProductType.objects.all()

    def create(self, request, *args, **kwargs):
        # TODO: Решить косяк с ManyToMany, вместо нескольких категорий, сохраняется одна
        for char_number, record in enumerate(request.data):
            external_category_ids = record.get('category')
            existing_category_ids = []

            try:
                for external_id in external_category_ids:
                    recipient_category = RecipientCategory.objects.get(
                        external_id=external_id,
                    )
                    existing_category_ids.append(recipient_category.id)
            except RecipientCategory.DoesNotExist:
                return Response(
                    {'error': 'Категория не найдена'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except RecipientCategory.MultipleObjectsReturned:
                return Response(
                    {'error': 'Найдено несколько категорий с указанным external_id'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                
            request.data[char_number]['category'] = existing_category_ids
        
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RecipientCharacteristicAPIViewSet(ModelViewSet):
    serializer_class = RecipientCharacteristicSerializer
    queryset = RecipientCharacteristic.objects.all()

    def create(self, request, *args, **kwargs):
        for char_number, record in enumerate(request.data):
            external_category_ids = record.get('recipient_category')
            existing_category_ids = []

            try:
                for external_id in external_category_ids:
                    recipient_category = RecipientCategory.objects.get(
                        external_id=external_id,
                    )
                    existing_category_ids.append(recipient_category.id)
            except RecipientCategory.DoesNotExist:
                return Response(
                    {'error': 'Категория не найдена'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except RecipientCategory.MultipleObjectsReturned:
                return Response(
                    {'error': 'Найдено несколько категорий с указанным external_id'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.data[char_number]['recipient_category'] = existing_category_ids

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RecipientCharacteristicValueAPIViewSet(ModelViewSet):
    serializer_class = RecipientCharacteristicValueSerializer
    queryset = RecipientCharacteristicValue.objects.all()

    def create(self, request, *args, **kwargs):
        for char_value_number, record in enumerate(request.data):
            external_characteristic_id = record.get('recipient_characteristic')

            try:
                provider_characteristic = RecipientCharacteristic.objects.get(
                    external_id=external_characteristic_id,
                )
                existing_characteristic_id = provider_characteristic.id
            except RecipientCharacteristic.DoesNotExist:
                return Response(
                    {'error': 'Характеристика не найдена'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except RecipientCharacteristic.MultipleObjectsReturned:
                return Response(
                    {'error': 'Найдено несколько характеристик с указанным external_id'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            request.data[char_value_number]['recipient_characteristic'] = existing_characteristic_id

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
