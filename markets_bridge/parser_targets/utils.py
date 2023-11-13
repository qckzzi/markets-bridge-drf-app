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


def send_target_products_to_parsing():
    products = get_allowed_products()

    for product in products:
        publish_to_parsing_queue(json.dumps({'url': product.url, 'type': EntityType.PRODUCT}))


def send_target_categories_to_parsing():
    categories = get_allowed_categories()

    for category in categories:
        publish_to_parsing_queue(json.dumps({'url': category.url, 'type': EntityType.CATEGORY}))


def publish_to_parsing_queue(message: str):
    publish(message, 'parsing')
