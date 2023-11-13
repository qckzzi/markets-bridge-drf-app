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
