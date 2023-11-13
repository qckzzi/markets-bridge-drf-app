import requests


def update_recipient_attributes(external_category_id: int):
    # TODO: Вынести в конфиг
    requests.get(
        'http://127.0.0.1:8001/load_ozon_attributes_for_category/',
        params={'category_id': external_category_id},
    )