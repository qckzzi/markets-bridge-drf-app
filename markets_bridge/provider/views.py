from django.db.models import (
    Q,
)
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

from common.models import (
    CharacteristicValueMatching,
)
from provider.models import (
    Category,
    Characteristic,
    CharacteristicValue,
    Product,
    ProductImage,
)
from provider.serializer import (
    CategorySerializer,
    CharacteristicSerializer,
    CharacteristicValueSerializer,
    ProductImageSerializer,
    ProductSerializer,
)
from provider.services import (
    create_or_update_product,
    get_or_create_category,
    get_or_create_characteristic_value,
    get_products_for_ozon,
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

    # TODO: Вместо этого эндпоинта сделать команду отправки непереведенных записей к сервису перевода
    @action(detail=False, methods=('GET',))
    def random_untranslated(self, request):

        untranslated_product = self.get_queryset().filter(
            Q(translated_name='') | Q(translated_name__isnull=True),
        ).order_by(
            '-update_date',
        ).first()

        serializer = self.get_serializer(untranslated_product)

        return Response(serializer.data)

    # TODO: Написать вместо этого логику получения нужных данных в сервисе ozon-outloader
    @action(detail=False, methods=('GET',))
    def for_ozon(self, request):
        products = get_products_for_ozon(request.get_host())

        return Response(products)


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

    # TODO: Вместо этого эндпоинта сделать команду отправки непереведенных записей к сервису перевода
    @action(detail=False, methods=('GET',))
    def random_untranslated(self, request):

        untranslated_category = self.get_queryset().filter(
            Q(translated_name='') | Q(translated_name__isnull=True),
        ).order_by(
            'products',
            '?',
        ).first()

        serializer = self.get_serializer(untranslated_category)

        return Response(serializer.data)

    # TODO: Вместо этого эндпоинта сделать команду отправки запроса с категориями к сервису Ozon-inloader
    @action(detail=False, methods=('GET',))
    def with_products(self, requests):
        categories = self.get_queryset().filter(
            products__isnull=False,
        )

        serializer = self.get_serializer(categories, many=True)

        return Response(serializer.data)


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

    # TODO: Вместо этого эндпоинта сделать команду отправки непереведенных записей к сервису перевода
    @action(detail=False, methods=('GET',))
    def random_untranslated(self, request):

        untranslated_characteristic = self.get_queryset().filter(
            Q(translated_name='') | Q(translated_name__isnull=True),
        ).order_by(
            '-categories__products',
            '?',
        ).first()

        serializer = self.get_serializer(untranslated_characteristic)

        return Response(serializer.data)


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

    # TODO: Вместо этого эндпоинта сделать команду отправки непереведенных записей к сервису перевода
    @action(detail=False, methods=('GET',))
    def random_untranslated(self, request):

        not_translated_values = self.get_queryset().filter(
            Q(translated_value='') | Q(translated_value__isnull=True),
        ).order_by(
            '-characteristic__categories__products',
            '?',
        ).first()

        serializer = self.get_serializer(not_translated_values)

        return Response(serializer.data)
