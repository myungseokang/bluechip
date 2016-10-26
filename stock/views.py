from django.shortcuts import render
from django.views.generic.list import ListView

from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Stock, StockManager
from .forms import searchForm, requestForm

def main(request):
    search_Form = searchForm()
    first = Stock.objects.all().order_by('-price')[0] # 현재가가 가장 높은 주식
    return render(request, 'stock/main.html', {"first":first, 'searchForm':search_Form})

class StockLV(ListView):
    template_name = 'stock/stock_list.html'
    model = Stock

def stockDV(request, code):
    request_Form = requestForm()
    stock = Stock.objects.get(code=code)
    buy_prices, sell_price = stock.asking_price()
    return render(request, 'stock/stock_detail.html', {'stock':stock, 'requestForm':request_Form, 'buy_prices':buy_prices,'sell_prices':sell_price})

def stock_search(request):
    if request.method == 'POST':
        search_Form = searchForm(request.POST)
        """
        if search_Form.is_valid(): 오류 발생
        """
        title=request.POST['title']
        stocks = Stock.objects.filter(title__contains=title)
        if stocks.count() == 1:
            return HttpResponseRedirect(reverse('stock:stock_detail', args=(stocks[0].code,)))
        else:
            return render(request, 'stock/stock_search.html', {'stocks':stocks})
    return HttpResponseRedirect(reverse('stock:main'))

def Balances(request):
    return render(request, 'stock/Balances.html')

def stock_request(request, code):
    if request.method == "POST":
        form = requestForm(request.POST)
        if form.is_valid():
            request_flag = int(form.cleaned_data['request_flag'])
            request_price = int(form.cleaned_data['request_price'])
            count = int(form.cleaned_data['count'])
            if(request_flag==0):
                print("매도")
            elif(request_flag==1):
                print("매수")
                new_stock = StockManager.objects.create(user=request.user, stock=Stock.objects.get(code=code))
                new_stock.save()
                result = new_stock.buy(request_price, count)
                print(result)
                if(result!='1'):
                    return HttpResponseRedirect(reverse('stock:stock_detail', args=(code,)))
                new_stock.buy_conclusion()
    return HttpResponseRedirect(reverse('stock:Balances'))
