from datetime import datetime
import pytz

from django.http import HttpResponse
from django.shortcuts import render

import kcurrency.forex as fx
import kcurrency.markets as market


def index(request):
    return HttpResponse("Hello, World!")


def exchange_rate(request, base, dst):
    context = {
        "base": base,
        "dst": dst,
        "price": fx.current_rate(base, dst),
        "time": datetime.now(pytz.utc).strftime('%Y-%m-%d')
    }
    return render(request, 'exchange_rate.html', context)


def stock(request, ticker):
    context = {
        "ticker": ticker,
        "price": fx.current_rate(ticker) if fx.is_crypto(ticker) else market.get_price(ticker=ticker),
        "time": datetime.now(pytz.utc).strftime('%Y-%m-%d')
    }
    return render(request, 'market_data.html', context)
