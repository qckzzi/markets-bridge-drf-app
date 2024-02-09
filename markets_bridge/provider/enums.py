from core.enums import (
    BaseEnumerate,
)


class ProductActionType(BaseEnumerate):
    LOAD_PRODUCTS = 'LOAD_PRODUCTS'
    UPDATE_PRODUCT_PRICES = 'UPDATE_PRODUCT_PRICES'
    UPDATE_PRODUCT_STOCKS = 'UPDATE_PRODUCT_STOCKS'
    ARCHIVE_PRODUCTS = 'ARCHIVE_PRODUCTS'

    labels = {
        LOAD_PRODUCTS: 'Первичная загрузка товаров',
        UPDATE_PRODUCT_PRICES: 'Обновление цен',
        UPDATE_PRODUCT_STOCKS: 'Обновление остатков',
        ARCHIVE_PRODUCTS: 'Архивирование товаров',
    }

class ProductStatusEnum(BaseEnumerate):
    ACTIVE = 1
    ARCHIVED = 2

    labels = {
        ACTIVE: 'Активный',
        ARCHIVED: 'Архивирован',
    }
