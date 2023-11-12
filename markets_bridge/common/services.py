import requests

from common.models import (
    CategoryMatching,
)


def get_recipient_category_id_by_category_mathing_id(category_mathing_id):
    return CategoryMatching.objects.only(
        'recipient_category_id',
    ).get(
        pk=category_mathing_id,
    ).recipient_category_id


def update_recipient_attributes(external_category_id: int):
    # TODO: Вынести в конфиг
    requests.get('http://127.0.0.1:8001/load_ozon_attributes/', params={'category_id': external_category_id})
