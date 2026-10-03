import yfinance as yf


def get_price(ticker):
    t = yf.Ticker(ticker=ticker)

    # Yahoo needs the exchange suffix (e.g. ARN.TO, not ARN) and is inconsistent
    # about which field carries the quote for non-US listings, so try each source
    # in turn. Any of them may raise (e.g. HTTP 404 for an unknown symbol); a
    # source that errors or has no usable value just falls through to the next.
    for source in (_from_info, _from_fast_info, _from_history):
        try:
            price = source(t)
        except Exception:
            continue
        if price:
            return price

    return None


def _from_info(t):
    return t.info.get('regularMarketPrice')


def _from_fast_info(t):
    return t.fast_info.get('lastPrice')


def _from_history(t):
    todays_data = t.history(period='1d')
    if todays_data.empty:
        return None
    return todays_data['Close'].iloc[0]


if __name__ == '__main__':
    price = get_price(ticker='AGAG.V')
    print(price)
