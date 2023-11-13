import json
import os

from core.enums import (
    EntityType,
)
from markets_bridge.amqp import (
    publish,
)
from provider.enums import (
    ProductActionType,
)
from provider.services import (
    get_products_for_ozon,
    get_products_for_price_update,
    get_products_for_stock_update,
)


def translate_product(entity_id: int, text: str):
    translate_entity(entity_id, text, EntityType.PRODUCT)


def translate_category(entity_id: int, text: str):
    translate_entity(entity_id, text, EntityType.CATEGORY)


def translate_characteristic(entity_id: int, text: str):
    translate_entity(entity_id, text, EntityType.CHARACTERISTIC)


def translate_characteristic_value(entity_id: int, text: str):
    translate_entity(entity_id, text, EntityType.CHARACTERISTIC_VALUE)


def translate_entity(entity_id: int, text: str, entity_type: str):
    message = {'id': entity_id, 'text': text, 'type': entity_type}
    publish_to_translation_queue(json.dumps(message))


def publish_to_translation_queue(message: str):
    publish(message, 'translation')


def load_products():
    products = get_products_for_ozon(os.getenv('HOST'))

    if products:
        message = {'products': products, 'method': ProductActionType.LOAD_PRODUCTS}
        publish_to_outloading_queue(json.dumps(message))


def update_product_prices():
    products = get_products_for_price_update()

    if products:
        message = {'products': products, 'method': ProductActionType.UPDATE_PRODUCT_PRICES}
        publish_to_outloading_queue(json.dumps(message))


def update_product_stocks():
    products = get_products_for_stock_update()

    if products:
        message = {'products': products, 'method': ProductActionType.UPDATE_PRODUCT_STOCKS}
        publish_to_outloading_queue(json.dumps(message))


def publish_to_outloading_queue(message: str):
    publish(message, 'outloading')
