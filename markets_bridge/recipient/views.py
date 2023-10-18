from django.db.models import (
    F,
)
from rest_framework import (
    status,
)
from rest_framework.response import (
    Response,
)
from rest_framework.views import (
    APIView,
)
from rest_framework.viewsets import (
    ModelViewSet,
)

from recipient.models import (
    RecipientCategory,
    RecipientCharacteristic,
    RecipientCharacteristicValue,
)
from recipient.serializers import (
    RecipientCategorySerializer,
    RecipientCharacteristicSerializer,
    RecipientCharacteristicValueSerializer,
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


class RecipientCharacteristicAPIViewSet(ModelViewSet):
    serializer_class = RecipientCharacteristicSerializer
    queryset = RecipientCharacteristic.objects.all()

    def create(self, request, *args, **kwargs):
        chars = []
        for char_number, record in enumerate(request.data):
            char = RecipientCharacteristic(
                name=record.get('name'),
                external_id=record.get('external_id'),
            )
            chars.append(char)

        result = RecipientCharacteristic.objects.bulk_create(chars)

        for char, raw_char in zip(chars, request.data):
            existed_categories = RecipientCategory.objects.filter(
                external_id__in=raw_char['recipient_categories'],
            )

            char.recipient_category.set(existed_categories)

        return Response(status=status.HTTP_201_CREATED)


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


class MatchingRecipientCategoriesAPIView(APIView):
    def get(self, request, format=None):
        category_ids = RecipientCategory.objects.filter(
            provider_categories__isnull=False,
        ).values(
            'external_id', 
            category_external_id=F('category__external_id'),
        )

        return Response(category_ids)
