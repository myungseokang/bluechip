from django.shortcuts import render

# Create your views here.

def trade(request):
    return render(request, 'stock_analsis/trade.html')

def increase(request):
    return render(request, 'stock_analsis/increase.htm')

def decrease(request):
    return render(request, 'stock_analsis/decrease.html')
