from celery import (
    shared_task,
)

from parser_targets.utils import (
    send_existed_products_to_update,
    send_target_categories_to_parsing,
    send_target_products_to_parsing,
)


@shared_task
def send_target_products_to_parsing_task():
    send_target_products_to_parsing()


@shared_task
def send_target_categories_to_parsing_task():
    send_target_categories_to_parsing()



@shared_task
def send_existed_products_to_update_task():
    send_existed_products_to_update()
