from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Stock

def main(request):
    first = Stock.objects.all().order_by('-price')[0]
    graph_url = first.graph_url()
    return render(request, 'stock/main.html', {"first":first,"graph":graph_url})

class StockLV(ListView):
    template_name = 'stock/stock_list.html'
    model = Stock
