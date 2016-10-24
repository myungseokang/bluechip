from django.shortcuts import render
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.forms import AuthenticationForm

from accounts.forms import Sing_upForm


class Home(FormView):
    template_name = 'home.html'
    form_class = AuthenticationForm
    success_url = '/home/'

class Sign_up(CreateView):
    template_name = 'Sign_up.html'
    form_class = Sing_upForm
    success_url = '/home/'
