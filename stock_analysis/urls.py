from django.conf.urls import url

from .views import trade, increase, decrease

urlpatterns = [
    url(r'^$', trade, name='first'),
    url(r'^trade/$', trade, name="trade"),
    url(r'^increase/$', increase, name='increase'),
    url(r'^decrease/$', decrease, name='decrease'),
]
