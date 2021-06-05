from currency_converter import CurrencyConverter, RateNotFoundError
from forex_python.bitcoin import BtcConverter
import kcurrency.dolarblue as dolarblue


def current_rate(base, dst):
    if base == 'BTC':
        b = BtcConverter(force_decimal=False)
        rate = b.get_latest_price(dst)
        return rate

    if 'ARS' in (base, dst):
        rate = dolarblue.latest_rate(base, dst)
        return rate

    c = CurrencyConverter()

    try:
        rate = c.convert(1, base, dst)
    except RateNotFoundError:
        return '<N/A>'

    return rate


if __name__ == '__main__':
    print(current_rate('BTC', 'ARS'))
