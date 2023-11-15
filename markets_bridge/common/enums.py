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


class VatRate(BaseEnumerate):
    """Ставки НДС."""

    NON_TAXABLE = '0'
    TEN_PERCENT = '0.1'
    TWENTY_PERCENT = '0.2'

    labels = {
        NON_TAXABLE: 'Не облагается',
        TEN_PERCENT: '10%',
        TWENTY_PERCENT: '20%',
    }