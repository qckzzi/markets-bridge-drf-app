import logging

from django.db.models import (
    QuerySet,
)
from django.db.transaction import (
    atomic,
)

from common.enums import (
    MarketplaceTypeEnum,
)
from common.models import (
    CategoryMatching,
    CharacteristicMatching,
    CharacteristicValueMatching,
    Currency,
    ExchangeRate,
    Log,
    Marketplace,
    SystemEnvironment,
)
from common.utils import (
    get_exchange_rate,
)
from recipient.models import (
    CharacteristicForCategory,
    CharacteristicValue,
)


def get_recipient_category_id_by_category_mathing_id(category_mathing_id):
    return CategoryMatching.objects.only(
        'recipient_category_id',
    ).get(
        pk=category_mathing_id,
    ).recipient_category_id


def get_system_environments():
    return SystemEnvironment.objects.all()


@atomic
def create_characteristic_matchings_by_category_matching_id(category_matching_id: int):
    category_matching = CategoryMatching.objects.get(
        id=category_matching_id,
    )
    recipient_characteristic_ids = CharacteristicForCategory.objects.filter(
        category=category_matching.recipient_category_id,
    ).values_list(
        'id',
        flat=True,
    )

    char_matching_list = [
        CharacteristicMatching(category_matching_id=category_matching_id, recipient_characteristic_id=char_id)
        for char_id in recipient_characteristic_ids
    ]

    created_char_mathing_list = CharacteristicMatching.objects.bulk_create(char_matching_list)

    for char_mathing in created_char_mathing_list:
        recipient_char_value_ids = CharacteristicValue.objects.filter(
            characteristic_id=char_mathing.recipient_characteristic_id,
        ).values_list(
            'id',
            flat=True,
        )

        char_value_mathing_list = [
            CharacteristicValueMatching(
                characteristic_matching_id=char_mathing.id,
                recipient_characteristic_value_id=value_id,
            )
            for value_id in recipient_char_value_ids
        ]

        CharacteristicValueMatching.objects.bulk_create(char_value_mathing_list)


def update_or_create_exchange_rates():
    currencies = list(get_currencies())

    for src_currency in currencies:
        currencies.remove(src_currency)

        for dest_currency in currencies:
            update_exchange_rate(src_currency, dest_currency)
            update_exchange_rate(dest_currency, src_currency)


def get_currencies():
    return Currency.objects.all()


def update_exchange_rate(source: Currency, destination: Currency):
    """Получает актуальную на данный момент информацию о курсе и записывает ее базе."""

    decimal_rate, rate_datetime = get_exchange_rate(source.code, destination.code)
    exchange_rate, is_new = ExchangeRate.objects.update_or_create(
        source=source,
        destination=destination,
        defaults={'rate': decimal_rate, 'rate_datetime': rate_datetime},
    )

    logging.info(f'{exchange_rate} exchange rate has been {"created" if is_new else "updated"}')

def get_providers():
    all_marketplaces = get_marketplaces()

    return all_marketplaces.filter(
        type=MarketplaceTypeEnum.PROVIDER,
    )


def get_recipients():
    all_marketplaces = get_marketplaces()

    return all_marketplaces.filter(
        type=MarketplaceTypeEnum.RECIPIENT,
    )


def get_marketplaces():
    return Marketplace.objects.select_related(
        'currency',
    )


def write_log(message: str):
    Log.objects.create(
        service_name='Markets-Bridge',
        entry=message,
    )
