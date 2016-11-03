from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import searchForm, requestForm
from .models import Stock, StockManager, InvestUser
from django.db.models import Q

import random

def main(request):
    if(not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('home'))
    stocks = Stock.objects.all()
    stock_business = []

    for stock in stocks:
        if stock.business not in stock_business:
            stock_business.append(stock.business)

    business = request.GET.get('business')
    if(business!=None):
        stocks = Stock.objects.filter(business=business)
    else:
        business='건설업'
        stocks = Stock.objects.filter(business=business)
    context = {
        'business':business,
        'stock_business': stock_business,
        'searchForm':searchForm(),
        'stocks':stocks
    }
    return render(request, 'stock/main.html', context)

def random_stock(request):
    if(not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('home'))
    stocks = Stock.objects.all()
    rand_num = random.randint(0, stocks.count())
    stock = stocks[rand_num]
    return HttpResponseRedirect(reverse('stock:stock_detail', args=(stock.code, )))

def stock_detail(request, code):
    if(not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('home'))
    stock = Stock.objects.get(code=code)
    stock.stock_reset()
    context = {
        'stock': stock,
        'searchForm':searchForm()
    }
    return render(request, 'stock/stock_detail.html', context)

def buy_sell(request, code):
    if(not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('home'))
    stock = Stock.objects.get(code=code)
    stock.stock_reset()
    buy_prices, sell_price = stock.asking_price()
    own_count, request_buy,request_sell=stock.about_stock(request.user)
    context = {
        'stock':stock,
        'buy_prices': buy_prices,
        'sell_prices': sell_price,
        'own_count' : own_count,
        'request_buy': request_buy,
        'request_sell': request_sell,
        'searchForm':searchForm(),
    }
    return render(request, 'stock/stock_buy_sell.html', context)


def stock_search(request):
    if(not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        """
        if search_form.is_valid(): 오류 발생
        """
        title = request.POST.get('title', '')
        stocks = Stock.objects.filter(title__contains=title)
        if stocks.count() == 1:
            return HttpResponseRedirect(reverse('stock:stock_detail', args=(stocks[0].code,)))
        else:
            return render(request, 'stock/stock_search.html', {'stocks': stocks,'searchForm':searchForm()})
    return HttpResponseRedirect(reverse('stock:main'))


def stock_request(request, code):
    if(not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('home'))

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
            new_stock.conclusion()
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
    if(not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        if request.POST['request_cancel'] == '취소':
            stock = StockManager.objects.get(pk=int(request.POST.get('stock')))
            stock.cancel()
    own_stock = request.user.own_stock()
    log_stock = request.user.log_stock()
    stock_balances = StockManager.objects.filter(user=request.user).filter(Q(request_flag=0, flag=1) | Q(request_flag=1) | Q(request_cancel=1)).order_by('-create_time')
    context = {
        'own_stocks':own_stock,
        'log_stocks':log_stock,
        'searchForm':searchForm(),
        'stock_balances':stock_balances
    }
    return render(request, 'stock/Balances.html', context)

def ranking(request):
    if(not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('home'))
    InvestUse = InvestUser.objects.all()
    users = []
    for user in InvestUse:
        user.total_money_reset()
    top_ten = InvestUser.objects.all().order_by('-total_money')[:10]
    context =  {
        'top_ten':top_ten
    }
    return render(request, 'stock/ranking.html', context)
