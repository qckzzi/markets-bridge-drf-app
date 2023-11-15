from celery import (
    shared_task,
)

from recipient.utils import (
    update_recipient_brands,
    update_recipient_categories,
)


@shared_task
def update_recipient_categories_task():
    update_recipient_categories()


@shared_task
def update_recipient_brands_task():
    update_recipient_brands()