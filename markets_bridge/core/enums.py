class BaseEnumerate:
    """Base class for enumerations.

    Used to indicate choices on a model attribute and to maintain code.
    """

    labels = dict()

    @classmethod
    def get_choices(cls):
        return cls.labels.items()


class EntityType(BaseEnumerate):
    PRODUCT = 'PRODUCT'
    CATEGORY = 'CATEGORY'
    CHARACTERISTIC = 'CHARACTERISTIC'
    CHARACTERISTIC_VALUE = 'CHARACTERISTIC_VALUE'

    labels = {
        PRODUCT: 'Товар',
        CATEGORY: 'Категория/поиск',
        CHARACTERISTIC: 'Характеристика',
        CHARACTERISTIC_VALUE: 'Значение характеристики',
    }


class TranslationTargets(BaseEnumerate):
    PRODUCT_NAME = 'PRODUCT_NAME'
    PRODUCT_DESCRIPTION = 'PRODUCT_DESCRIPTION'
    CATEGORY_NAME = 'CATEGORY_NAME'
    CHARACTERISTIC_NAME = 'CHARACTERISTIC_NAME'
    CHARACTERISTIC_VALUE = 'CHARACTERISTIC_VALUE'

    labels = {
        PRODUCT_NAME: 'Наименование товара',
        PRODUCT_DESCRIPTION: 'Описание товара',
        CATEGORY_NAME: 'Наименование категории',
        CHARACTERISTIC_NAME: 'Наименование характеристики',
        CHARACTERISTIC_VALUE: 'Значение характеристики',
    }
