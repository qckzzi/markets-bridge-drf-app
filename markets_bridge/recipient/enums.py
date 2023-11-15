from core.enums import (
    BaseEnumerate,
)


class LoadingOperationType(BaseEnumerate):
    LOAD_FOR_CATEGORY = 'LOAD_FOR_CATEGORY'
    LOAD_CATEGORIES = 'LOAD_CATEGORIES'

    labels = {
        LOAD_FOR_CATEGORY: 'Загрузка атрибутов внешней системы для определенной категории',
        LOAD_CATEGORIES: 'Загрузка всех категорий внешней системы',
    }