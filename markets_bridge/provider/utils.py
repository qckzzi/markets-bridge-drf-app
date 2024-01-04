import json
import os

from common.services import (
    get_personal_areas,
)
from core.enums import (
    TranslationTargets,
)
from markets_bridge.amqp import (
    publish,
)
from provider.enums import (
    ProductActionType,
)
from provider.models import (
    Product,
)
from provider.services import (
    get_products_for_import,
    get_products_for_price_update,
    get_products_for_stock_update,
    get_request_body_for_product_update,
)


def translate_product(entity_id: int, text: str):
    translate_entity(entity_id, text, TranslationTargets.PRODUCT_NAME)


def translate_product_description(entity_id, text: str):
    translate_entity(entity_id, text, TranslationTargets.PRODUCT_DESCRIPTION)


def translate_category(entity_id: int, text: str):
    translate_entity(entity_id, text, TranslationTargets.CATEGORY_NAME)


def translate_characteristic(entity_id: int, text: str):
    translate_entity(entity_id, text, TranslationTargets.CHARACTERISTIC_NAME)


def translate_characteristic_value(entity_id: int, text: str):
    translate_entity(entity_id, text, TranslationTargets.CHARACTERISTIC_VALUE)


def translate_entity(entity_id: int, text: str, entity_type: str):
    message = {'id': entity_id, 'text': text, 'type': entity_type}
    publish_to_translation_queue(json.dumps(message))


def publish_to_translation_queue(message: str):
    publish(message, 'translation')


def load_products():
    personal_areas = get_personal_areas()

    for area in personal_areas:
        products = get_products_for_import(area)

        if products:
            message = {'products': products, 'method': ProductActionType.LOAD_PRODUCTS}
            publish_to_outloading_queue(json.dumps(message))


def update_product(product: Product):
    body = get_request_body_for_product_update(product)

    if body:
        message = {'products': body, 'method': ProductActionType.LOAD_PRODUCTS}
        publish_to_outloading_queue(json.dumps(message))


def update_product_prices():
    personal_areas = get_personal_areas()

    for area in personal_areas:
        products = get_products_for_price_update(area)

        if products:
            message = {'products': products, 'method': ProductActionType.UPDATE_PRODUCT_PRICES}
            publish_to_outloading_queue(json.dumps(message))


def update_product_stocks():
    personal_areas = get_personal_areas()

    for area in personal_areas:
        products = get_products_for_stock_update(area)

        if products:
            message = {'products': products, 'method': ProductActionType.UPDATE_PRODUCT_STOCKS}
            publish_to_outloading_queue(json.dumps(message))


def publish_to_outloading_queue(message: str):
    publish(message, 'outloading')
