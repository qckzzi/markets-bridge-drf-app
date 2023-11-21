import datetime
import logging
from decimal import (
    Decimal,
)
from typing import (
    Literal,
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
    SystemSettingConfig,
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


@atomic
def create_or_update_product(product_data: dict) -> tuple[Product, bool]:
    """Создает товар, либо обновляет его."""

    marketplace_id = product_data.get('marketplace_id')

    category_external_id = product_data.pop('category_external_id')
    category = get_object_or_404(
        Category,
        external_id=category_external_id,
        marketplace_id=marketplace_id,
    )
    product_data['category_id'] = category.id

    brand_external_id = product_data.pop('brand_external_id')
    brand = get_object_or_404(
        Brand,
        external_id=brand_external_id,
        marketplace_id=marketplace_id,
    )
    product_data['brand_id'] = brand.id

    external_id = product_data.get('external_id')
    value_external_ids = product_data.pop('characteristic_value_external_ids')

    product, is_new = Product.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=product_data,
    )

    if is_new:
        characteristic_values = CharacteristicValue.objects.filter(
            external_id__in=value_external_ids,
            marketplace_id=marketplace_id,
        )

        ProductValue.objects.bulk_create(
            ProductValue(product=product, value_id=value_id)
            for value_id in characteristic_values.values_list('id', flat=True)
        )
    else:
        product.price = product_data['price']
        product.discounted_price = product_data['discounted_price']
        product.stock_quantity = product_data['stock_quantity']
        product.save()

    return product, is_new


def get_or_create_category(category_data: dict) -> tuple[Category, bool]:
    """Создает категорию."""

    external_id = category_data.get('external_id')
    marketplace_id = category_data.get('marketplace_id')

    category, is_new = Category.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=category_data,
    )

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
@atomic
def get_products_for_ozon(host: str) -> dict:
    result = []

    products = Product.objects.filter(
        is_export_allowed=True,
    ).select_related(
        'brand',
        'marketplace__currency',
        'marketplace__logistics',
    )

    for product in products:
        attributes = []
        category_matching = product.category.matching
        recipient_category = category_matching.recipient_category

        if not recipient_category:
            error = f'У товара {product} с ID: {product.id} не сопоставлена категория'
            logging.info(error)
            write_log(error)

            continue

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

        char_mathings_with_default_raw_value = category_matching.characteristic_matchings.filter(
            value__isnull=False,
        )

        for matching in char_mathings_with_default_raw_value:
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
                value__icontains=product.brand.name,
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

        product_price = get_converted_product_price(product)
        
        raw_product = dict(
            attributes=attributes,
            name=product_name,
            description_category_id=recipient_category.external_id,
            images=[f'https://{host}{image_record.image.url}' for image_record in product.images.all()],
            offer_id=str(product.id),
            price=str(product_price),
            vat=vat,
        )

        if product.price != product.discounted_price:
            old_price = get_converted_product_discounted_price(product)
            raw_product['old_price'] = str(old_price)

        result.append(raw_product)

        product.upload_date = datetime.datetime.now()
        product.save()

    return dict(items=result) if result else {}


@atomic
def get_products_for_price_update():
    result = []

    products = Product.objects.filter(
        is_export_allowed=True,
        upload_date__isnull=False,
    ).select_related(
        'marketplace__currency',
        'marketplace__logistics',
    )

    for product in products:
        product_price = get_converted_product_price(product)
        raw_product = dict(
            offer_id=str(product.id),
            price=str(product_price),
        )

        if product.price != product.discounted_price:
            old_price = get_converted_product_discounted_price(product)
            raw_product['old_price'] = str(old_price)
        else:
            raw_product['old_price'] = '0'

        result.append(raw_product)

        product.upload_date = datetime.datetime.now()
        product.save()

    return dict(prices=result) if result else {}


@atomic
def get_products_for_stock_update():
    result = []

    products = Product.objects.filter(
        is_export_allowed=True,
        upload_date__isnull=False,
    )

    for product in products:
        raw_product = dict(
            offer_id=str(product.id),
            stock=product.stock_quantity,
        )

        result.append(raw_product)

        product.upload_date = datetime.datetime.now()
        product.save()

    return dict(stocks=result) if result else {}


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
    marketplace_id = brand_data.get('marketplace_id')

    brand, is_new = Brand.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=brand_data,
    )

    return brand, is_new


def get_product_urls_for_update() -> list[str]:
    return Product.objects.filter(
        is_updated=True,
    ).values_list(
        'url',
        flat=True,
    )
