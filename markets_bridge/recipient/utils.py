import json

from markets_bridge.amqp import (
    publish,
)
from recipient.enums import (
    LoadingOperationType,
)


def update_recipient_attributes(category_external_id: int, matching_id: int):
    message = {
        'category_external_id': category_external_id,
        'matching_id': matching_id,
        'method': LoadingOperationType.LOAD_FOR_CATEGORY,
    }
    publish_to_loading_queue(json.dumps(message))


def update_recipient_categories():
    message = {
        'method': LoadingOperationType.LOAD_CATEGORIES,
    }
    publish_to_loading_queue(json.dumps(message))


def publish_to_loading_queue(message: str):
    publish(message, 'inloading')