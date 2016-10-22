from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm


class Home(FormView):
    template_name = 'home.html'
    form_class = AuthenticationForm
    success_url = '/home/'

