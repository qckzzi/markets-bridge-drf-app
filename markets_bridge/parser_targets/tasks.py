import json

from celery import (
    shared_task,
)

from core.enums import (
    EntityType,
)
from parser_targets.services import (
    get_allowed_categories,
    get_allowed_products,
)
from parser_targets.utils import (
    publish_to_parsing_queue,
)


@shared_task
def send_target_products_to_parsing():
    products = get_allowed_products()

    for product in products:
        publish_to_parsing_queue(json.dumps({'url': product.url, 'type': EntityType.PRODUCT}))


@shared_task
def send_target_categories_to_parsing():
    categories = get_allowed_categories()

    for category in categories:
        publish_to_parsing_queue(json.dumps({'url': category.url, 'type': EntityType.CATEGORY}))
