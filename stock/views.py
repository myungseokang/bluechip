from django.shortcuts import render
from django.views.generic.list import ListView

from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Stock
from .forms import searchForm

def main(request):
    search_Form = searchForm()
    first = Stock.objects.all().order_by('-price')[0] # 현재가가 가장 높은 주식
    return render(request, 'stock/main.html', {"first":first, 'searchForm':search_Form})

class StockLV(ListView):
    template_name = 'stock/stock_list.html'
    model = Stock

def stockDV(request, code):
    print(code)
    stock = Stock.objects.get(code=code)
    return render(request, 'stock/stock_detail.html', {'stock':stock})

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
