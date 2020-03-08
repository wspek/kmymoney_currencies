# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, World!")


def eurusd(request):
    context = {"price": 1.1293}
    return render(request,'eurusd.html', context)
