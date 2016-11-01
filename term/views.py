from django.shortcuts import render

from .models import Term
# Create your views here.

def term(request):
    terms = Term.objects.all()
    context = {
        'terms':terms
    }
    return render(request, 'term/term.html', context)
