from celery import (
    shared_task,
)

from provider.utils import (
    load_products,
    update_product_prices,
    update_product_stocks,
)


@shared_task
def load_products_task():
    load_products()


@shared_task
def update_product_stocks_task():
    update_product_stocks()


@shared_task
def update_product_prices_task():
    update_product_prices()

