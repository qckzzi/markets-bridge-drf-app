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
from recipient.models import (
    Category,
    Characteristic,
    CharacteristicValue,
)
from recipient.serializers import (
    CategorySerializer,
    CharacteristicSerializer,
    CharacteristicValueSerializer,
)
from recipient.services import (
    update_or_create_category,
    update_or_create_characteristic,
    update_or_create_characteristic_value,
)


class CategoryAPIViewSet(AuthenticationMixin, ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def create(self, request, *args, **kwargs):
        category, is_new = update_or_create_category(request.data)
        serializer = self.get_serializer(category)

        if is_new:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_200_OK

        return Response(data=serializer.data, status=http_status)


class CharacteristicAPIViewSet(AuthenticationMixin, ModelViewSet):
    serializer_class = CharacteristicSerializer
    queryset = Characteristic.objects.all()

    def create(self, request, *args, **kwargs):
        characteristic, is_new = update_or_create_characteristic(request.data)
        serializer = self.get_serializer(characteristic)

        if is_new:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_200_OK

        return Response(data=serializer.data, status=http_status)


class CharacteristicValueAPIViewSet(AuthenticationMixin, ModelViewSet):
    serializer_class = CharacteristicValueSerializer
    queryset = CharacteristicValue.objects.all()

    def create(self, request, *args, **kwargs):
        characteristic_value, is_new = update_or_create_characteristic_value(request.data)
        serializer = self.get_serializer(characteristic_value)

        if is_new:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_200_OK

        return Response(data=serializer.data, status=http_status)
