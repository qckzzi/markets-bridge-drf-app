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
