from django.shortcuts import render

from stock.models import Stock
from stock.forms import searchForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def trade(request):
    trade_list = Stock.objects.all().order_by('-deal')
    paginator = Paginator(trade_list, 30)

    page = request.GET.get('page', '')
    try:
        trade_page = paginator.page(page)
    except PageNotAnInteger:
        trade_page = paginator.page(1)
    except EmptyPage:
        trade_page = paginator.page(paginator.num_pages)
    context = {
        'trade_page': trade_page,
        'pagination_range': paginator.page_range,
        'searchForm': searchForm(),
    }
    return render(request, 'stock_analysis/trade.html', context)


def increase(request):
    increase_list = Stock.objects.filter(change__gt=0).order_by('-change')
    paginator = Paginator(increase_list, 30)
    page = request.GET.get('page', '')
    try:
        increase_page = paginator.page(page)
    except PageNotAnInteger:
        increase_page = paginator.page(1)
    except EmptyPage:
        increase_page = paginator.page(paginator.num_pages)
    context = {
        'increase_page': increase_page,
        'pagination_range': paginator.page_range,
        'searchForm': searchForm(),
    }
    return render(request, 'stock_analysis/increase.html', context)


def decrease(request):
    decrease_list = Stock.objects.filter(change__lt=0).order_by('change')
    paginator = Paginator(decrease_list, 30)
    page = request.GET.get('page', '')
    try:
        decrease_page = paginator.page(page)
    except PageNotAnInteger:
        decrease_page = paginator.page(1)
    except EmptyPage:
        decrease_page = paginator.page(paginator.num_pages)
    context = {
        'decrease_page': decrease_page,
        'pagination_range': paginator.page_range,
        'searchForm': searchForm(),
    }
    return render(request, 'stock_analysis/decrease.html', context)
