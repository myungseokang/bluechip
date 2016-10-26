from django.conf.urls import url

from .views import trade

urlpatterns = [
    url(r'^$', trade, name='first'),
    url(r'^trade/$', trade, name="trade"),
]
