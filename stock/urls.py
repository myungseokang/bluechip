from django.conf.urls import url

from .views import StockLV, main, stock_detail, stock_search, balances, stock_request


urlpatterns = [
    url(r'^main/$', main, name='main'),
    url(r'^$', StockLV.as_view(), name='list'),
    url(r'^detail/(?P<code>[A-Za-z-0-9]+)/$', stock_detail, name='stock_detail'),
    url(r'^search/$', stock_search, name='search'),
    url(r'^request/(?P<code>[A-Za-z-0-9]+)/$', stock_request, name="request"),
    url(r'^balances/$', balances, name="Balances"),
]
