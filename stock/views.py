from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView

from .forms import searchForm, requestForm
from .models import Stock, StockManager


def main(request):
    search_form = searchForm()
    # 현재가가 가장 높은 주식
    first = Stock.objects.all().order_by('-price')[0]
    return render(request, 'stock/main.html', {"first": first, 'searchForm': search_form})


class StockLV(ListView):
    template_name = 'stock/stock_list.html'
    model = Stock


def stock_detail(request, code):
    stock = Stock.objects.get(code=code)
    buy_prices, sell_price = stock.asking_price()
    own_count=stock.about_stock(request.user)[0] # 소유 주식
    context = {
        'stock': stock,
        'buy_prices': buy_prices,
        'sell_prices': sell_price,
        'own_count' : own_count,
    }
    return render(request, 'stock/stock_detail.html', context)


def stock_search(request):
    if request.method == 'POST':
        """
        if search_form.is_valid(): 오류 발생
        """
        title = request.POST.get('title', '')
        stocks = Stock.objects.filter(title__contains=title)
        if stocks.count() == 1:
            return HttpResponseRedirect(reverse('stock:stock_detail', args=(stocks[0].code,)))
        else:
            return render(request, 'stock/stock_search.html', {'stocks': stocks})
    return HttpResponseRedirect(reverse('stock:main'))


def stock_request(request, code):
    if request.method == "POST":
        request_flag = int(request.POST.get('request_flag', ''))
        request_price = int(request.POST.get('request_price', ''))
        count = int(request.POST.get('count', ''))
        print(request_flag, request_price, count)
        if request_flag == 0:
            print("매도")
            new_stock = StockManager.objects.create(user=request.user, stock=Stock.objects.get(code=code))
            result = new_stock.sell(request_price, count)
            if result != 1:
                messages.add_message(request, messages.INFO, result)
                return redirect('stock:stock_detail', code=code)
        elif request_flag == 1:
            print("매수")
            new_stock = StockManager.objects.create(user=request.user, stock=Stock.objects.get(code=code))
            result = new_stock.buy(request_price, count)
            if result != 1:
                messages.add_message(request, messages.INFO, result)
                return redirect('stock:stock_detail', code=code)
            new_stock.conclusion()
    return HttpResponseRedirect(reverse('stock:Balances'))

def balances(request):
    own_stock = request.user.own_stock()
    log_stock = request.user.log_stock()
    print(log_stock)
    context = {
        'own_stocks':own_stock,
        'log_stocks':log_stock,
    }
    return render(request, 'stock/Balances.html', context)
