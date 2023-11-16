from celery import (
    shared_task,
)

from common.services import (
    update_or_create_exchange_rates,
)


@shared_task
def update_or_create_exchange_rates_task():
    update_or_create_exchange_rates()
