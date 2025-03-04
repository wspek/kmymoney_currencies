from currency_converter import CurrencyConverter, RateNotFoundError, SINGLE_DAY_ECB_URL
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import kcurrency.dolarblue as dolarblue

CRYPTO = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'XRP': 'XRP',
}


def is_crypto(ticker):
    return ticker in CRYPTO


def current_rate(base, dst='USD'):
    if is_crypto(base):
        name = CRYPTO[base]
        try:
            cmc = CoinMarketCapAPI('c8ba2595-96c4-482b-8c98-4d4d555d0474')
            r = cmc.cryptocurrency_quotes_latest(symbol=base)
            entry = next((item for item in r.data[base] if item['name'] == name), None)

            if entry:
                return entry['quote']['USD']['price']
            else:
                raise CoinMarketCapAPIError("BTC not found in the response")
        except CoinMarketCapAPIError:
            raise Exception('CoinMarketCap threw an exception')

    if 'ARS' in (base, dst):
        return dolarblue.latest_rate(base, dst)

    c = CurrencyConverter(currency_file=SINGLE_DAY_ECB_URL)

    try:
        return c.convert(1, base, dst)
    except RateNotFoundError:
        return '<N/A>'


if __name__ == '__main__':
    rate = current_rate(base='XRP', dst='EUR')
    print(rate)
