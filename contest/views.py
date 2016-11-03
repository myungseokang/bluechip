from django.shortcuts import render
from .models import Contest


def contest(request):
    context = {
        'contest_list': Contest.objects.all(),
    }
    return render(request, 'contest/contest.html', context)
