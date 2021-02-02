from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path('(?P<base>[A-Z]{3}) > (?P<dst>[A-Z]{3})', views.exchange_rate),
    re_path('(?P<ticker>[A-Z\.]+)$', views.stock),
]
