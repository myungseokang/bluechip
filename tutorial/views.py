from django.shortcuts import render

# Create your views here.
def tutorial_1(request):
    return render(request, 'tutorial/tutorial_1.html')

def tutorial_2(request):
    return render(request, 'tutorial/tutorial_2.html')

def tutorial_3(request, stock):
    context = {
        'stock':stock,
    }
    return render(request, 'tutorial/tutorial_3.html', context)

def tutorial_4(request, stock, price1):
    context = {
        'stock':stock,
        'price1':price1,
    }
    return render(request, 'tutorial/tutorial_4.html', context)

def tutorial_5(request, stock, price1):
    context = {
        'stock':stock,
        'price1':price1,
    }
    return render(request, 'tutorial/tutorial_5.html', context)

def tutorial_6(request, stock, price1):
    context = {
        'stock':stock,
        'price1':price1,
    }
    return render(request, 'tutorial/tutorial_6.html', context)

def tutorial_7(request, stock, price1):
    context = {
        'stock':stock,
        'price1':price1,
    }
    return render(request, 'tutorial/tutorial_7.html', context)

def tutorial_8(request, stock, price1, price2):
    context = {
        'stock':stock,
        'price1':price1,
        'price2':price2,
    }
    return render(request, 'tutorial/tutorial_8.html', context)

def tutorial_9(request, stock, price1, price2):
    result = int(price2)-int(price1)
    context = {
        'price1':price1,
        'stock':stock,
        'price2':price2,
        'result':result
    }
    return render(request, 'tutorial/tutorial_9.html', context)

def tutorial_10(request, stock, price1, price2):
    context = {
        'price1':price1,
        'stock':stock,
        'price2':price2,
    }
    return render(request, 'tutorial/tutorial_10.html', context)
