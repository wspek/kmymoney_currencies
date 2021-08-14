import yfinance as yf


def get_price(ticker):
    msft = yf.Ticker(ticker=ticker)
    info = msft.info
    todays_data = msft.history(period='1d')

    try:
        price = info['bid'] or todays_data['Close'][0]
    except KeyError:  # Sometimes 'bid' does not exist when the market is closed.
        price = todays_data['Close'][0]

    return price


if __name__ == '__main__':
    price = get_price(ticker='LWLG')
    print(price)
