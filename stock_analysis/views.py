from django.shortcuts import render

from stock.models import Stock
# Create your views here.

def trade(request):
    trade_list = Stock.objects.all().order_by('-deal')
    context = {
        'trade_list':trade_list,
    }
    return render(request, 'stock_analysis/trade.html', context)

def increase(request):
    return render(request, 'stock_analysis/increase.htm')

def decrease(request):
    return render(request, 'stock_analysis/decrease.html')
