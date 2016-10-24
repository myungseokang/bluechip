from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.forms import AuthenticationForm

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
