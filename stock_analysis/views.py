from django.shortcuts import render

from stock.models import Stock

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def trade(request):
    trade_list = Stock.objects.all().order_by('-deal')
    paginator = Paginator(trade_list, 30)

    page = request.GET.get('page')
    try:
        trade_list = paginator.page(page)
    except PageNotAnInteger:
        trade_list = paginator.page(1)
    except EmptyPage:
        trade_list = paginator.page(paginator.num_pages)
    page_start = paginator.start_index()/10 * 10
    context = {
        'trade_list':trade_list,
    }
    return render(request, 'stock_analysis/trade.html', context)

def increase(request):
    return render(request, 'stock_analysis/increase.htm')

def decrease(request):
    return render(request, 'stock_analysis/decrease.html')
