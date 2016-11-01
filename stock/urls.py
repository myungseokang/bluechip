from django.conf.urls import url

from .views import main, stock_detail, stock_search, balances, stock_request, ranking, random_stock


urlpatterns = [
    url(r'^main/$', main, name='main'),
    url(r'random_stock/$', random_stock, name='random_stock'),
    url(r'^detail/(?P<code>[A-Za-z-0-9]+)/$', stock_detail, name='stock_detail'),
    url(r'^search/$', stock_search, name='search'),
    url(r'^request/(?P<code>[A-Za-z-0-9]+)/$', stock_request, name="request"),
    url(r'^balances/$', balances, name="Balances"),
    url(r'^ranking/$', ranking, name="ranking"),
]
