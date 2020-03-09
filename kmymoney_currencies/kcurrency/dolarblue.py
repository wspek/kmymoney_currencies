import requests
from enum import Enum


currency = {
    # 'USD': 'oficial',
    # 'USB': 'blue',
    # 'EUR': 'oficial_euro',
    # 'EUB': 'blue_euro',
    'USD': 'blue',
    'EUR': 'blue_euro',     # Due to the CEPO (09/03/2020) we can only realistically calculate with blue in KMyMoney.
}


class Value(Enum):
    AVG = 'value_avg'
    SELL = 'value_sell'
    BUY = 'value_buy'


def latest_rate(base, dst):
    url = 'http://api.bluelytics.com.ar/v2/latest'
    response = requests.get(url).json()

    if base == 'ARS':
        dst_value = response[currency[dst]][Value.SELL.value]
        rate = 1 / dst_value
    elif dst == 'ARS':
        rate = response[currency[base]][Value.BUY.value]
    else:
        raise ValueError('None of the currencies are ARS (base = {}, dst = {})'.format(base, dst))

    return rate
