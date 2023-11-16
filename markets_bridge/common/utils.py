from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)

import requests
from bs4 import (
    BeautifulSoup,
)
from dateutil.parser import (
    parse,
)


def get_exchange_rate(src: str, dest: str) -> tuple[Decimal, datetime]:
    """Парсит источник курса валют.

    Args:
        src: код исходной валюты;
        dest: код целевой валюты.

    Returns:
        tuple: курс и дата последнего обновления.
    """

    content = requests.get(f'https://ru.investing.com/currencies/{src.lower()}-{dest.lower()}').content
    soup = BeautifulSoup(content, 'html.parser')
    exchange_rate_datetime_tag = soup.find('time', attrs={'class': 'instrument-metadata_text__Y52j_ font-bold'})
    raw_exchange_rate_datetime = exchange_rate_datetime_tag['datetime']
    exchange_rate_datetime = parse(raw_exchange_rate_datetime)

    exchange_rate = soup.find('span', attrs={'class': 'text-2xl'}).text
    exchange_rate = exchange_rate.replace(',', '.')
    decimal_exchange_rate = Decimal(exchange_rate)

    return decimal_exchange_rate, exchange_rate_datetime
