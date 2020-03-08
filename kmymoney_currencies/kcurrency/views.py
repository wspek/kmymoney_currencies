# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, World!")


def eurusd(request):
    context = {"price": 1.1293}
    return render(request,'eurusd.html', context)


def exchange_rate(request, src, dst):
    context = {
        "src": src,
        "dst": dst,
        "price": 1.1293
    }
    return render(request, 'exchange_rate.html', context)
