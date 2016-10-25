from django.conf.urls import url

from .views import StockLV, main, stockDV, stock_search, Balances, stock_request


urlpatterns = [
    url(r'^main/$', main, name='main'),
    url(r'^$', StockLV.as_view(), name='list'),
    url(r'^detail/(?P<code>[A-Za-z-0-9]+)/$', stockDV, name='stock_detail'),
    url(r'^search/$', stock_search, name='search'),
    url(r'^request/(?P<code>[A-Za-z-0-9]+)/$', stock_request, name="request"),
    url(r'^balances/$', Balances, name="Balances"),
]
