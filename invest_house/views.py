from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

from accounts.forms import Sing_upForm

def Home(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('stock:main'))
    form = AuthenticationForm()
    return render(request, 'home.html', {'form':form})

class Sign_up(CreateView):
    template_name = 'Sign_up.html'
    form_class = Sing_upForm
    success_url = '/home/'

    def get(self, request):
        if(request.user.is_authenticated):
            return HttpResponseRedirect(reverse('stock:main'))
        else:
            return render(request, 'Sign_up.html', {'form': Sing_upForm})

def mypage(request):
    if(not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'mypage.html')

def exit(request):
    request.user.stockmanager_set.all().delete()
    request.user.user_reset()
    return HttpResponseRedirect(reverse('stock:main'))

def setting_login(request):
    if request.method == "POST":
        username =request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('stock:main'))
        else:
            messages.add_message(request, messages.INFO, '로그인 실패')
            return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))
