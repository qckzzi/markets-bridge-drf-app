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
from django.http import Http404, HttpResponseBadRequest
from rest_framework.generics import (
    get_object_or_404,
)

from common.models import (
    CategoryMatching,
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
from core.constants import PRODUCT_TYPE_CHARACTERISTIC_EXTERNAL_ID
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
    Category as RecipientCategory,
    Characteristic as RecipientCharacteristic,
)

from recipient.utils import update_recipient_attributes_for_product


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

    category = Category.objects.filter(
        **category_getting_kwargs,
    ).first()

    if not category:
        raise Http404('Category is not found')

    product_data['category_id'] = category.id

    brand_getting_kwargs = dict(
        marketplace_id=marketplace_id,
    )

    if product_data.get('brand_external_id'):
        brand_external_id = product_data.pop('brand_external_id')
        brand_getting_kwargs['external_id'] = brand_external_id
    elif product_data.get('brand_name', None) is not None:
        brand_name = product_data.pop('brand_name')
        brand_getting_kwargs['name'] = brand_name

    brand = Brand.objects.filter(
        **brand_getting_kwargs,
    ).first()

    if not brand:
        raise Http404('Brand is not found')

    product_data['brand_id'] = brand.id

    external_id = product_data.get('external_id')

    value_external_ids = []
    characteristics = []

    if product_data.get('characteristic_value_external_ids'):
        value_external_ids = product_data.pop('characteristic_value_external_ids')
    elif product_data.get('characteristics'):
        characteristics = product_data.pop('characteristics')

    product_data['translated_name'] = product_data['name']
    product_data['translated_description'] = product_data['description']

    product, is_new = Product.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=product_data,
    )

    if not is_new:
        if product_data.get('price'):
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
    elif characteristics:
        product_values = []
        for ch in characteristics:
            characteristic_value = CharacteristicValue.objects.filter(
                value=ch["value"],
                characteristic__name=ch["name"],
                marketplace_id=marketplace_id,
            ).first()

            if not characteristic_value:
                raise Http404(f"Characteristic value for '{ch.name}' characteristic is not found")

            product_values.append(ProductValue(product=product, value_id=characteristic_value.id))
    
        ProductValue.objects.bulk_create(product_values)

        recipient_product_type = category.matching.recipient_category
        update_recipient_attributes_for_product(
            category_external_id=recipient_product_type.parent_category.external_id,
            product_type_external_id=recipient_product_type.external_id,
            product_id=product.id,
        )

    return product, is_new


@atomic
def get_or_create_category(category_data: dict) -> tuple[Category, bool]:
    """Создает категорию."""

    external_id = category_data.get('external_id')
    name = category_data.get('name')
    category_data['translated_name'] = name
    marketplace_id = category_data.get('marketplace_id')

    get_or_create_kwargs = dict(
        marketplace_id=marketplace_id,
        defaults=category_data,
    )

    if external_id:
        get_or_create_kwargs['external_id'] = external_id
    else:
        get_or_create_kwargs['name'] = name
        
    recipient_category = RecipientCategory.objects.filter(
        name=name,
        marketplace_id=marketplace_id,
    ).first()
    
    if not recipient_category:
        raise Http404

    is_new = False

    category = Category.objects.filter(
        translated_name=recipient_category.name,
        marketplace_id=marketplace_id,
    ).first()

    if not category:
        category = Category.objects.create(
            name=recipient_category.name,
            translated_name=recipient_category.name,
            marketplace_id=marketplace_id,
            external_id=recipient_category.external_id,
        )

        is_new = True
    
    if not CategoryMatching.objects.filter(provider_category=category).exists():
        CategoryMatching.objects.create(
            provider_category=category,
            recipient_category=recipient_category,
        )

    return category, is_new


@atomic
def update_or_create_characteristic(characteristic_data: dict) -> tuple[Characteristic, bool]:
    """Создает новую характеристику, либо обновляет ее связи с категориями."""

    marketplace_id = characteristic_data.get('marketplace_id')
    external_id = characteristic_data.get('external_id') or 0
    type_name = characteristic_data.pop('product_type_name')
    characteristic_data['external_id'] = external_id
    characteristic_data['translated_name'] = characteristic_data['name']
    
    if not type_name:
        raise HttpResponseBadRequest

    category = Category.objects.filter(
        translated_name=type_name,
        marketplace_id=marketplace_id,
    ).first()

    if not category:
        raise Http404("Category not found")

    is_new = False

    characteristic = Characteristic.objects.filter(
        name=characteristic_data['name'],
        marketplace_id=marketplace_id,
    ).first()

    if not characteristic:
        characteristic = Characteristic.objects.create(**characteristic_data)

        is_new = True

    if is_new:
        characteristic.categories.set([category])
    else:
        characteristic.categories.add(category)

    return characteristic, is_new


@atomic
def get_or_create_characteristic_value(value_data: dict) -> tuple[CharacteristicValue, bool]:
    """Создает новое значение характеристики, либо обновляет его."""

    external_id = value_data.get('external_id') or 0
    value_data['external_id'] = external_id
    value_data['translated_value'] = value_data['value']
    marketplace_id = value_data.get('marketplace_id')
    kwargs_to_characteristic_getting = dict(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=value_data,
    )

    kwargs_to_characteristic_getting['value'] = value_data['value']

    characteristic_name = value_data.pop('characteristic_name')
    characteristic = Characteristic.objects.filter(
        name=characteristic_name,
        marketplace_id=marketplace_id,
    ).first()

    kwargs_to_characteristic_getting['characteristic_id'] = characteristic.id

    is_new = False

    characteristic_value = CharacteristicValue.objects.filter(
        value=value_data['value'],
        marketplace_id=marketplace_id,
        characteristic_id=characteristic.id,
    ).first()

    if not characteristic_value:
        value_data["characteristic_id"] = characteristic.id
        characteristic_value = CharacteristicValue.objects.create(**value_data)

        is_new = True

    return characteristic_value, is_new


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


@atomic
def get_product_for_import(product_id: int) -> dict:
    items = []
    product = Product.objects.filter(
        id=product_id,
    ).select_related(
        'brand',
        'marketplace__currency',
        'marketplace__logistics',
    ).get()
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
        raise
    else:
        items.append(serialized_product)

    return dict(items=items, personal_area=raw_personal_area_variables) if items else {}


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


def get_request_bodies_for_products_archive(products: QuerySet[Product]) -> list[dict]:
    personal_areas = PersonalArea.objects.filter(
        warehouse__products__in=products,
    ).distinct()

    for personal_area in personal_areas:
        product_ids = products.filter(
            warehouse__personal_area=personal_area,
        ).values_list(
            'pk',
            flat=True,
        )
        personal_area_variables = SystemVariable.objects.filter(
            related_personal_areas__personal_area=personal_area,
        )
        system_variable_serializer = SystemVariableSerializer(personal_area_variables, many=True)
        raw_personal_area_variables = system_variable_serializer.data
        body = dict(product_ids=list(product_ids), personal_area=raw_personal_area_variables)

        yield body


def serialize_product_for_import(product: Product) -> dict:
    attributes = []
    category_matching = product.category.matching
    product_type = category_matching.recipient_category

    if not product_type:
        error = f'У товара {product} с ID: {product.id} не сопоставлена категория'
        raise ValueError(error)

    product_characteristics = Characteristic.objects.filter(characteristic_values__in=product.characteristic_values.all()).distinct()

    for characteristic in product_characteristics:
        values = CharacteristicValue.objects.filter(characteristic=characteristic, products=product)

        raw_values = []
        characteristic_external_id = None

        for value in values:
            if recipient_value := value.recipient_characteristic_values.all().select_related("characteristic").first():
                raw_values.append(dict(dictionary_value_id=recipient_value.external_id))

                if not characteristic_external_id:
                    characteristic_external_id = recipient_value.characteristic.external_id
            else:
                if not characteristic_external_id:
                    recipient_characteristic = RecipientCharacteristic.objects.filter(
                        name__icontains=characteristic.name,
                    ).first()

                    if not recipient_characteristic:
                        break
                    else:
                        characteristic_external_id = recipient_characteristic.external_id

                if characteristic_external_id:
                    raw_values.append(dict(value=value.value))

        if raw_values:
            attributes.append(dict(complex_id=0, id=characteristic_external_id, values=raw_values))

    try:
        if not product.brand.name:
            raise RecipientCharacteristicValue.DoesNotExist

        brand_external_id = RecipientCharacteristicValue.objects.only(
            'external_id',
        ).get(
            value__iexact=product.brand.name,
            characteristic__external_id=85,
            marketplace_id=1,
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

    attributes.append(
        dict(
            complex_id=0,
            id=4180,
            values=[dict(value=product.translated_name)]
        )
    )

    attributes.append(
        dict(
            complex_id=0,
            id=PRODUCT_TYPE_CHARACTERISTIC_EXTERNAL_ID,
            values=[dict(dictionary_value_id=product_type.external_id)]
        )
    )

    if product.translated_description:
        attributes.append(
            dict(
                complex_id=0,
                id=4191,
                values=[dict(value=product.translated_description)]
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
        name=product.translated_name,
        description_category_id=product_type.parent_category.external_id,
        images=[f'{host}{image_record.image.url}' for image_record in product.images.all()],
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
        has_all_dimensions = all((
            product.width,
            product.height,
            product.depth,
            product.weight,
        ))
        raw_product = dict(
            offer_id=str(product.id),
            stock=product.stock_quantity if has_all_dimensions else 0,
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

    converted_logistics_cost = convert_value(
        product_logistics.currency_code,
        'RUB',
        product_logistics.cost
    )

    converted_logistics_shipment_cost = convert_value(
        product_logistics.currency_code,
        'RUB',
        product_logistics.shipment_cost
    )

    volumetric_weight = (product.width*product.height*product.depth)/5000
    physical_weight = product.weight
    used_weight = volumetric_weight if volumetric_weight > physical_weight else physical_weight

    logistics_cost = converted_logistics_cost*10*used_weight + converted_logistics_shipment_cost
    logistics_cost_with_markup = logistics_cost + logistics_cost*Decimal(product_logistics.markup/100)

    converted_product_price = convert_value(
        product.currency_code,
        'RUB',
        getattr(product, price_field_name)
    )

    product_price_with_markup = converted_product_price + converted_product_price*Decimal(product.markup/100)

    return product_price_with_markup + logistics_cost_with_markup


@atomic
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

    is_new = False
    brand = Brand.objects.filter(
        marketplace_id=marketplace_id,
        name=name,
    ).first()

    if not brand:
        brand = Brand.objects.create(
            marketplace_id=marketplace_id,
            name=name,
        )

        is_new = True

    return brand, is_new


def get_provider_products() -> QuerySet[Product]:
    return Product.objects.all()


def get_products_to_update() -> QuerySet[Product]:
    return get_provider_products().filter(
        is_updated=True,
    )


def update_product_export_allowance(products: QuerySet[Product], is_allowed: bool):
    return products.update(
        is_export_allowed=is_allowed,
    )


def update_products_status(products: QuerySet[Product], status: int):
    return products.update(
        status=status,
    )


@atomic
def compare_product_characteristics(product_id: int):
    product = Product.objects.get(
        id=product_id,
    )
    
    characteristic_values = product.characteristic_values
    
    for value in characteristic_values.all():
        if value.recipient_characteristic_values.exists():
            continue
        
        characteristic_name = value.characteristic.name
        recipient_value = RecipientCharacteristicValue.objects.filter(
            characteristic__name__icontains=characteristic_name,
            value__icontains=value.value,
        ).first()

        if not recipient_value:
            continue

        value.recipient_characteristic_values.set([recipient_value])
