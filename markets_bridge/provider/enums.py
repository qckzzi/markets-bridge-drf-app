from core.enums import (
    BaseEnumerate,
)


class ProductActionType(BaseEnumerate):
    LOAD_PRODUCTS = 'LOAD_PRODUCTS'
    UPDATE_PRODUCT_PRICES = 'UPDATE_PRODUCT_PRICES'
    UPDATE_PRODUCT_STOCKS = 'UPDATE_PRODUCT_STOCKS'

    labels = {
        LOAD_PRODUCTS: 'Первичная загрузка товаров',
        UPDATE_PRODUCT_PRICES: 'Обновление цен',
        UPDATE_PRODUCT_STOCKS: 'Обновление остатков',
    }