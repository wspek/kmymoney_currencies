from forex_python.converter import CurrencyRates, RatesNotAvailableError
import kcurrency.dolarblue as dolarblue


def current_rate(base, dst):
    if 'ARS' in (base, dst):
        rate = dolarblue.latest_rate(base, dst)
        return rate

    c = CurrencyRates()

    try:
        rate = c.get_rate(base, dst)
    except RatesNotAvailableError:
        return '<N/A>'

    return rate


if __name__ == '__main__':
    print(current_rate('ARS', 'USD'))
