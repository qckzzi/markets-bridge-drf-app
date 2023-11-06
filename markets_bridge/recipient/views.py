from rest_framework import (
    status,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    ModelViewSet,
)

from recipient.models import (
    Category,
    Characteristic,
    CharacteristicValue,
)
from recipient.serializers import (
    CategorySerializer,
    CharacteristicSerializer,
    CharacteristicValueSerializer,
    RelevantCategorySerializer,
)
from recipient.services import (
    get_matched_category_external_ids,
    update_or_create_category,
    update_or_create_characteristic,
    update_or_create_characteristic_value,
)


class CategoryAPIViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    relevant_serializer_class = RelevantCategorySerializer
    queryset = Category.objects.all()

    def create(self, request, *args, **kwargs):
        category, is_new = update_or_create_category(request.data)

        if is_new:
            serializer = self.get_serializer(category)
            response = Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            response = Response(
                data={'message': f'The "{category.name}" category already exists.'},
                status=status.HTTP_200_OK,
            )

        return response

    @action(detail=False, methods=('GET',))
    def relevant(self, request):
        categories = get_matched_category_external_ids()
        serializer = self.relevant_serializer_class(categories, many=True)

        return Response(data=serializer.data)


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
        characteristic_value, is_new = update_or_create_characteristic_value(request.data)

        if is_new:
            serializer = self.get_serializer(characteristic_value)
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(
                data={'message': f'The "{characteristic_value.value}" characteristic value already exists.'},
                status=status.HTTP_200_OK,
            )

        return response
