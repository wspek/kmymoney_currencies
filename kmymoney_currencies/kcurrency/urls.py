from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('EURUSD', views.eurusd, name='eurusd'),
]