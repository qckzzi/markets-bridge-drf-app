import json

from core.enums import (
    EntityType,
)
from markets_bridge.amqp import (
    publish,
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
