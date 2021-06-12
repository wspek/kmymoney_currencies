from currency_converter import CurrencyConverter, RateNotFoundError
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import kcurrency.dolarblue as dolarblue


def is_crypto(ticker):
    return ticker in (
        'BTC',
        'BCH',
        'XMR',
        'GRIN',
    )


def current_rate(base, dst='USD'):
    if is_crypto(ticker=base):
        try:
            cmc = CoinMarketCapAPI('c8ba2595-96c4-482b-8c98-4d4d555d0474')
            r = cmc.cryptocurrency_quotes_latest(symbol=base)
            rate = r.data[base]['quote']['USD']['price']
            return rate
        except CoinMarketCapAPIError:
            raise Exception('CoinMarketCap threw an exception')

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
