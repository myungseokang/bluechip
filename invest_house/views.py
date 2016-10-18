from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    Login_Form = AuthenticationForm()
    return render(request, 'home.html', {'Login_Form':Login_Form})
