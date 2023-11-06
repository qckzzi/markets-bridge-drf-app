import datetime
from decimal import (
    Decimal,
)

from rest_framework.generics import (
    get_object_or_404,
)

from common.models import (
    CategoryMatching,
    CharacteristicValueMatching,
    SystemSettingConfig,
)
from provider.models import (
    Category,
    Characteristic,
    CharacteristicValue,
    Product,
    ProductValue,
)


def create_or_update_product(product_data: dict) -> tuple[Product, bool]:
    """Создает товар, либо обновляет его."""

    category_external_id = product_data.pop('category_external_id')
    marketplace_id = product_data.get('marketplace_id')

    category = get_object_or_404(
        Category,
        external_id=category_external_id,
        marketplace_id=marketplace_id,
    )

    product_data['category_id'] = category.id
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
        # TODO: Сделать обновление стоимости и наличия товара
        ...

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


def create_category_mathing(category_id) -> CategoryMatching:
    return CategoryMatching.objects.create(
        provider_category_id=category_id,
    )


def get_products_for_ozon(host) -> dict:
    result = []

    for product in Product.objects.filter(is_export_allowed=True):
        attributes = []
        category_matching = product.category.matching
        recipient_category = category_matching.recipient_category

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
                        values=[
                            dict(
                                dictionary_value_id=recipient_value.external_id,
                            )
                        ]
                    )
                )

        char_mathings_with_default_value = category_matching.characteristic_matchings.filter(
            recipient_value__isnull=False,
        )

        for matching in char_mathings_with_default_value:
            attributes.append(
                dict(
                    complex_id=0,
                    id=matching.recipient_characteristic.external_id,
                    values=[
                        dict(
                            dictionary_value_id=matching.recipient_value.external_id
                        )
                    ]
                )
            )

        char_mathings_with_default_raw_value = category_matching.characteristic_matchings.filter(
            value__isnull=False,
        )

        for matching in char_mathings_with_default_raw_value:
            attributes.append(
                dict(
                    complex_id=0,
                    id=matching.recipient_characteristic.external_id,
                    values=[
                        dict(
                            value=matching.value
                        )
                    ]
                )
            )

        attributes.append(
            dict(
                complex_id=0,
                id=85,
                values=[
                    dict(
                        value='Нет бренда'
                    )
                ]
            )
        )

        attributes.append(
            dict(
                complex_id=0,
                id=9048,
                values=[
                    dict(
                        value=product.translated_name
                    )
                ]
            )
        )

        raw_product = dict(
            attributes=attributes,
            name=product.translated_name,
            description_category_id=recipient_category.external_id,
            images=[f'{host}{image_record.image.url}' for image_record in product.images.all()],
            offer_id=str(product.id),
            price=str(get_converted_price(product.discounted_price)),
            vat='0.1'
        )

        if product.price != product.discounted_price:
            raw_product['old_price'] = str(get_converted_price(product.price))

        result.append(raw_product)

        product.upload_date = datetime.datetime.now()
        product.save()

    return dict(items=result)


def get_converted_price(price: Decimal):
    # TODO: Написать конвертер валют
    return price * Decimal('3.28') * SystemSettingConfig.objects.get(is_selected=True).markup
