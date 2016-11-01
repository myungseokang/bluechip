from django.shortcuts import render

# Create your views here.

def term(request):
    return render(request, 'term/term.html')
