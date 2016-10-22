from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Stock


class StockLV(ListView):
    template_name = 'stock/stock_list.html'
    model = Stock
