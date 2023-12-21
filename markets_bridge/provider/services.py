import datetime
import logging
import os
from decimal import (
    Decimal,
)
from typing import (
    Literal,
)

from django.db.models import (
    QuerySet,
)
from django.db.transaction import (
    atomic,
)
from rest_framework.generics import (
    get_object_or_404,
)

from common.models import (
    CategoryMatching,
    CharacteristicValueMatching,
    Logistics,
    PersonalArea,
    SystemSettingConfig,
    SystemVariable,
)
from common.serializers import (
    SystemVariableSerializer,
)
from common.services import (
    convert_value,
    write_log,
)
from provider.models import (
    Brand,
    Category,
    Characteristic,
    CharacteristicValue,
    Product,
    ProductValue,
)
from recipient.models import (
    CharacteristicValue as RecipientCharacteristicValue,
)


# TODO: Декомпозировать
@atomic
def create_or_update_product(product_data: dict) -> tuple[Product, bool]:
    """Создает товар, либо обновляет его."""

    marketplace_id = product_data.get('marketplace_id')

    category_getting_kwargs = dict(
        marketplace_id=marketplace_id,
    )

    if product_data.get('category_external_id'):
        category_external_id = product_data.pop('category_external_id')
        category_getting_kwargs['external_id'] = category_external_id
    elif product_data.get('category_name'):
        category_name = product_data.pop('category_name')
        category_getting_kwargs['name'] = category_name

    category = get_object_or_404(
        Category,
        **category_getting_kwargs,
    )
    product_data['category_id'] = category.id

    brand_getting_kwargs = dict(
        marketplace_id=marketplace_id,
    )

    if product_data.get('brand_external_id'):
        brand_external_id = product_data.pop('brand_external_id')
        brand_getting_kwargs['external_id'] = brand_external_id
    elif product_data.get('brand_name'):
        brand_name = product_data.pop('brand_name')
        brand_getting_kwargs['name'] = brand_name

    brand = get_object_or_404(
        Brand,
        **brand_getting_kwargs,
    )
    product_data['brand_id'] = brand.id

    external_id = product_data.get('external_id')

    value_external_ids = []

    if product_data.get('characteristic_value_external_ids'):
        value_external_ids = product_data.pop('characteristic_value_external_ids')

    product, is_new = Product.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=product_data,
    )

    if not is_new:
        product.price = product_data['price']
        product.discounted_price = product_data['discounted_price']
        product.stock_quantity = product_data['stock_quantity']
        product.save()
    elif value_external_ids:
        characteristic_values = CharacteristicValue.objects.filter(
            external_id__in=value_external_ids,
            marketplace_id=marketplace_id,
        )

        ProductValue.objects.bulk_create(
            ProductValue(product=product, value_id=value_id)
            for value_id in characteristic_values.values_list('id', flat=True)
        )

    return product, is_new


def get_or_create_category(category_data: dict) -> tuple[Category, bool]:
    """Создает категорию."""

    external_id = category_data.get('external_id')
    name = category_data.get('name')
    marketplace_id = category_data.get('marketplace_id')

    get_or_create_kwargs = dict(
        marketplace_id=marketplace_id,
        defaults=category_data,
    )

    if external_id:
        get_or_create_kwargs['external_id'] = external_id
    else:
        get_or_create_kwargs['name'] = name

    category, is_new = Category.objects.get_or_create(**get_or_create_kwargs)

    return category, is_new


@atomic
def update_or_create_characteristic(characteristic_data: dict) -> tuple[Characteristic, bool]:
    """Создает новую характеристику, либо обновляет ее связи с категориями."""

    external_id = characteristic_data.get('external_id')
    category_external_ids = characteristic_data.pop('category_external_ids')
    marketplace_id = characteristic_data.get('marketplace_id')

    characteristic, is_new = Characteristic.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=characteristic_data,
    )

    categories = Category.objects.filter(
        external_id__in=category_external_ids,
        marketplace_id=marketplace_id,
    )

    if is_new:
        characteristic.categories.set(categories)
    else:
        characteristic.categories.add(*categories)

    return characteristic, is_new


def get_or_create_characteristic_value(value_data: dict) -> tuple[CharacteristicValue, bool]:
    """Создает новое значение характеристики, либо обновляет его."""

    external_id = value_data.get('external_id')
    characteristic_external_id = value_data.pop('characteristic_external_id')
    marketplace_id = value_data.get('marketplace_id')

    characteristic = get_object_or_404(
        Characteristic,
        external_id=characteristic_external_id,
        marketplace_id=marketplace_id,
    )

    value_data['characteristic_id'] = characteristic.id

    characteristic_value, is_new = CharacteristicValue.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=value_data,
    )

    return characteristic_value, is_new


def create_category_matching(category_id) -> CategoryMatching:
    return CategoryMatching.objects.create(
        provider_category_id=category_id,
    )


# TODO: Логика выгрузки товара должна быть переделана, DRF не должен формировать данные под формат озона
#       Писалось на скорую руку...
#       #40
@atomic
def get_products_for_import(personal_area: PersonalArea) -> dict:
    items = []
    personal_area_variables = SystemVariable.objects.filter(
        related_personal_areas__personal_area=personal_area,
    )
    system_variable_serializer = SystemVariableSerializer(personal_area_variables, many=True)
    raw_personal_area_variables = system_variable_serializer.data

    products = Product.objects.filter(
        is_export_allowed=True,
        warehouse__personal_area=personal_area,
        upload_date__isnull=True,
    ).select_related(
        'brand',
        'marketplace__currency',
        'marketplace__logistics',
    )

    for product in products:
        try:
            serialized_product = serialize_product_for_import(product)
        except ValueError as e:
            error_message = ', '.join(e.args)
            logging.info(error_message)
            write_log(error_message)
            continue
        else:
            items.append(serialized_product)

    return dict(items=items, personal_area=raw_personal_area_variables) if items else {}


# TODO: Я себе обещаю, что скоро переделаю эту порнографию
#    (￢_￢)
@atomic
def get_request_body_for_product_update(product: Product):
    items = []
    personal_area_variables = SystemVariable.objects.filter(
        related_personal_areas__personal_area=product.warehouse.personal_area,
    )
    system_variable_serializer = SystemVariableSerializer(personal_area_variables, many=True)
    raw_personal_area_variables = system_variable_serializer.data

    try:
        serialized_product = serialize_product_for_import(product)
    except ValueError as e:
        error_message = ', '.join(e.args)
        logging.info(error_message)
        write_log(error_message)
    else:
        items.append(serialized_product)

    return dict(items=items, personal_area=raw_personal_area_variables) if items else {}


def serialize_product_for_import(product: Product) -> dict:
    attributes = []
    category_matching = product.category.matching
    recipient_category = category_matching.recipient_category

    if not recipient_category:
        error = f'У товара {product} с ID: {product.id} не сопоставлена категория'
        raise ValueError(error)

    product_characteristic_values = product.characteristic_values.all()

    for value in product_characteristic_values:
        try:
            recipient_value = value.matchings.get(
                characteristic_matching__category_matching=category_matching,
            ).recipient_characteristic_value
        except CharacteristicValueMatching.DoesNotExist:
            pass
        else:
            attributes.append(
                dict(
                    complex_id=0,
                    id=recipient_value.characteristic.external_id,
                    values=[dict(dictionary_value_id=recipient_value.external_id)]
                )
            )

    char_matchings_with_default_value = category_matching.characteristic_matchings.filter(
        recipient_value__isnull=False,
    )

    for matching in char_matchings_with_default_value:
        attributes.append(
            dict(
                complex_id=0,
                id=matching.recipient_characteristic.characteristic.external_id,
                values=[dict(dictionary_value_id=matching.recipient_value.external_id)]
            )
        )

    char_matchings_with_default_raw_value = category_matching.characteristic_matchings.filter(
        value__isnull=False,
    )

    for matching in char_matchings_with_default_raw_value:
        attributes.append(
            dict(
                complex_id=0,
                id=matching.recipient_characteristic.characteristic.external_id,
                values=[dict(value=matching.value)]
            )
        )

    try:
        brand_external_id = RecipientCharacteristicValue.objects.only(
            'external_id',
        ).get(
            value__iexact=product.brand.name,
            characteristic__external_id=85,
            marketplace_id=2,
        ).external_id
    except RecipientCharacteristicValue.DoesNotExist:
        attributes.append(
            dict(
                complex_id=0,
                id=85,
                values=[dict(value='Нет бренда')]
            )
        )
    else:
        attributes.append(
            dict(
                complex_id=0,
                id=85,
                values=[dict(dictionary_value_id=brand_external_id)]
            )
        )

    attributes.append(
        dict(
            complex_id=0,
            id=9048,
            values=[dict(value=product.translated_name)]
        )
    )

    product_name = f'{product.brand.name} {product.translated_name} {product.product_code}'

    attributes.append(
        dict(
            complex_id=0,
            id=4180,
            values=[dict(value=product_name)]
        )
    )

    vat = SystemSettingConfig.objects.only(
        'vat_rate',
    ).get(
        is_selected=True,
    ).vat_rate

    product_price = get_converted_product_discounted_price(product)

    host = os.getenv('HOST')

    raw_product = dict(
        attributes=attributes,
        name=product_name,
        description_category_id=recipient_category.external_id,
        images=[f'https://{host}{image_record.image.url}' for image_record in product.images.all()],
        offer_id=str(product.id),
        price=str(product_price),
        vat=vat,
        dimension_unit='mm',
        height=int(product.height * 10),
        width=int(product.width * 10),
        depth=int(product.depth * 10),
        weight=int(product.weight * 1000),
        weight_unit='g',
    )

    if product.price != product.discounted_price:
        old_price = get_converted_product_price(product)
        raw_product['old_price'] = str(old_price)

    product.upload_date = datetime.datetime.now()
    product.save()

    return raw_product


@atomic
def get_products_for_price_update(personal_area: PersonalArea):
    result = []
    raw_personal_area_variables = []

    products = Product.objects.filter(
        is_export_allowed=True,
        upload_date__isnull=False,
        warehouse__personal_area=personal_area,
    ).select_related(
        'marketplace__currency',
        'marketplace__logistics',
    )

    for product in products:
        product_price = get_converted_product_price(product)
        discounted_price = get_converted_product_discounted_price(product)
        raw_product = dict(
            offer_id=str(product.id),
            price=str(discounted_price),
            min_price=str(discounted_price),
        )

        if product.price != product.discounted_price:
            raw_product['old_price'] = str(product_price)
        else:
            raw_product['old_price'] = '0'

        result.append(raw_product)
        personal_area_variables = SystemVariable.objects.filter(
            related_personal_areas__personal_area=personal_area,
        ).values(
            'key',
            'value',
        )

        system_variable_serializer = SystemVariableSerializer(personal_area_variables, many=True)
        raw_personal_area_variables = system_variable_serializer.data

        product.upload_date = datetime.datetime.now()
        product.save()

    return dict(prices=result, personal_area=raw_personal_area_variables) if result else {}


@atomic
def get_products_for_stock_update(personal_area: PersonalArea):
    result = []
    raw_personal_area_variables = []

    products = Product.objects.filter(
        is_export_allowed=True,
        upload_date__isnull=False,
        warehouse__isnull=False,
        warehouse__personal_area=personal_area,
    ).select_related(
        'warehouse',
    )

    for product in products:
        raw_product = dict(
            offer_id=str(product.id),
            stock=product.stock_quantity,
            warehouse_id=product.warehouse.external_id,
        )

        result.append(raw_product)
        personal_area_variables = SystemVariable.objects.filter(
            related_personal_areas__personal_area=personal_area,
        ).values(
            'key',
            'value',
        )

        system_variable_serializer = SystemVariableSerializer(personal_area_variables, many=True)

        raw_personal_area_variables = system_variable_serializer.data
        product.upload_date = datetime.datetime.now()
        product.save()

    return dict(stocks=result, personal_area=raw_personal_area_variables) if result else {}


def get_converted_product_price(product: Product):
    return _get_converted_product_abstract_price(product, 'price')


def get_converted_product_discounted_price(product: Product):
    return _get_converted_product_abstract_price(product, 'discounted_price')


def _get_converted_product_abstract_price(product: Product, price_field_name: Literal['price', 'discounted_price']):
    product_logistics = Logistics.objects.get(
        marketplace__provider_products=product,
    )

    converted_product_price = convert_value(product.currency_code, 'RUB', getattr(product, price_field_name))
    converted_logistics_cost = convert_value(product_logistics.currency_code, 'RUB', product_logistics.cost)
    logistics_cost_per_product_weight = converted_logistics_cost * product.weight
    product_price_with_markup = converted_product_price + converted_product_price * Decimal(product.markup/100)

    return product_price_with_markup + logistics_cost_per_product_weight


def get_or_create_brand(brand_data: dict) -> tuple[Brand, bool]:
    external_id = brand_data.get('external_id')
    name = brand_data.get('name')
    marketplace_id = brand_data.get('marketplace_id')

    get_or_create_kwargs = dict(
        marketplace_id=marketplace_id,
        defaults=brand_data,
    )

    if external_id:
        get_or_create_kwargs['external_id'] = external_id
    else:
        get_or_create_kwargs['name'] = name

    brand, is_new = Brand.objects.get_or_create(**get_or_create_kwargs)

    return brand, is_new


def get_provider_products() -> QuerySet[Product]:
    return Product.objects.all()


def get_products_to_update() -> QuerySet[Product]:
    return get_provider_products().filter(
        is_updated=True,
    )


def update_product_export_allowance(products: QuerySet[Product], is_allowed: bool):
    products.update(
        is_export_allowed=is_allowed,
    )
