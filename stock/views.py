from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Stock

def main(request):
    first = Stock.objects.all().order_by('-price')[0] # 현재가가 가장 높은 주식
    return render(request, 'stock/main.html', {"first":first})

class StockLV(ListView):
    template_name = 'stock/stock_list.html'
    model = Stock
