import json

from core.enums import (
    EntityType,
)
from markets_bridge.amqp import (
    publish,
)
from parser_targets.services import (
    get_allowed_categories,
    get_allowed_products,
)
from provider.services import (
    get_products_to_update,
)


def send_target_products_to_parsing():
    products = get_allowed_products()

    for product in products:
        message = json.dumps(product.url)
        publish_to_parsing_queue(message, marketplace_id=product.marketplace_id, headers={"ENTITY_TYPE": EntityType.PRODUCT})


def send_existed_products_to_update():
    products = get_products_to_update()

    for product in products:
        message = json.dumps(product.url)
        publish_to_parsing_queue(message, marketplace_id=product.marketplace_id, headers={"ENTITY_TYPE": EntityType.PRODUCT})


def send_target_categories_to_parsing():
    categories = get_allowed_categories()

    for category in categories:
        message = json.dumps(category.url)
        publish_to_parsing_queue(message, marketplace_id=category.marketplace_id, headers={"ENTITY_TYPE": EntityType.CATEGORY})


def publish_to_parsing_queue(message: str, headers: dict, marketplace_id: int):
    publish(message, f'parsing.{marketplace_id}', headers=headers)
