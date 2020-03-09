from datetime import datetime
import pytz

from django.http import HttpResponse
from django.shortcuts import render

import kcurrency.forex as fx


def index(request):
    return HttpResponse("Hello, World!")


def exchange_rate(request, base, dst):
    context = {
        "base": base,
        "dst": dst,
        "price": fx.current_rate(base, dst),
        "time": datetime.now(pytz.utc).strftime('%y-%m-%d')
    }
    return render(request, 'exchange_rate.html', context)
