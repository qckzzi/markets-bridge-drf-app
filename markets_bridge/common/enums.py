from core.enums import (
    BaseEnumerate,
)


class MarketplaceTypeEnum(BaseEnumerate):
    """Типы маркетплейсов."""

    PROVIDER = 1
    RECIPIENT = 2

    labels = {
        PROVIDER: 'Поставщик',
        RECIPIENT: 'Получатель',
    }
