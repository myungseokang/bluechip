from django.shortcuts import render

# Create your views here.
def tutorial_1(request):
    return render(request, 'tutorial/tutorial_1.html')
