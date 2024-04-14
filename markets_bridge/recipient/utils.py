import json

from markets_bridge.amqp import (
    publish,
)
from recipient.enums import (
    LoadingOperationType,
)
from recipient.services import (
    get_matched_category_external_ids,
)


def update_recipient_attributes(category_external_id: int, product_type_external_id: int, matching_id: int):
    message = {
        'category_external_id': category_external_id,
        'product_type_external_id': product_type_external_id,
        'matching_id': matching_id,
        'method': LoadingOperationType.LOAD_FOR_CATEGORY,
    }
    publish_to_loading_queue(json.dumps(message))


def update_recipient_attributes_for_product(category_external_id: int, product_type_external_id: int, product_id: int):
    message = {
        'category_external_id': category_external_id,
        'product_type_external_id': product_type_external_id,
        'product_id': product_id,
        'method': LoadingOperationType.LOAD_FOR_PRODUCT,
    }
    publish_to_loading_queue(json.dumps(message))


def update_recipient_categories():
    message = {
        'method': LoadingOperationType.LOAD_CATEGORIES,
    }
    publish_to_loading_queue(json.dumps(message))


def update_recipient_brands():
    category_ids = get_matched_category_external_ids()
    entries = []

    for c in category_ids:
        entries.append({
            'category_external_id': c['category_external_id'],
            'product_type_external_id': c['product_type_external_id'],
        })

    if entries:
        message = {
            'categories': entries,
            'method': LoadingOperationType.LOAD_BRANDS,
        }
        publish_to_loading_queue(json.dumps(message))


def publish_to_loading_queue(message: str):
    publish(message, 'inloading')