from django.shortcuts import render

from stock.models import Stock
from stock.forms import searchForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def trade(request):
    trade_list = Stock.objects.all().order_by('-deal')
    paginator = Paginator(trade_list, 100)

    page = request.GET.get('page', '')

    try:
        if(int(page)==1):
            add = 0
        else:
            add = int(page) * 100
    except:
        pass

    try:
        trade_page = paginator.page(page)
    except PageNotAnInteger:
        add = 0
        trade_page = paginator.page(1)
    except EmptyPage:
        add =  paginator.end_index() * 100
        trade_page = paginator.page(paginator.num_pages)
    context = {
        'trade_page': trade_page,
        'pagination_range': paginator.page_range,
        'searchForm': searchForm(),
        'add':add
    }
    return render(request, 'stock_analysis/trade.html', context)


def increase(request):
    increase_list = Stock.objects.filter(change__gt=0).order_by('-change')
    paginator = Paginator(increase_list, 100)
    page = request.GET.get('page', '')

    try:
        if(int(page)==1):
            add = 0
        else:
            add = int(page) * 100
    except:
        pass

    try:
        increase_page = paginator.page(page)
    except PageNotAnInteger:
        add = 0
        increase_page = paginator.page(1)
    except EmptyPage:
        add =  paginator.end_index() * 100
        increase_page = paginator.page(paginator.num_pages)
    context = {
        'trade_page': increase_page,
        'pagination_range': paginator.page_range,
        'searchForm': searchForm(),
        'add':add
    }
    return render(request, 'stock_analysis/increase.html', context)

def decrease(request):
    decrease_list = Stock.objects.filter(change__lt=0).order_by('change')
    paginator = Paginator(decrease_list, 100)
    page = request.GET.get('page', '')

    try:
        if(int(page)==1):
            add = 0
        else:
            add = int(page) * 100
    except:
        pass

    try:
        decrease_page = paginator.page(page)
    except PageNotAnInteger:
        add = 0
        decrease_page = paginator.page(1)
    except EmptyPage:
        add =  paginator.end_index() * 100
        decrease_page = paginator.page(paginator.num_pages)
    context = {
        'trade_page': decrease_page,
        'pagination_range': paginator.page_range,
        'searchForm': searchForm(),
        'add':add,
    }
    return render(request, 'stock_analysis/decrease.html', context)
