import yfinance as yf


def get_price(ticker):
    msft = yf.Ticker(ticker=ticker)
    info = msft.info
    todays_data = msft.history(period='1d')

    price = info['bid'] or todays_data['Close'][0]

    return price


if __name__ == '__main__':
    price = get_price(ticker='NB.TO')
