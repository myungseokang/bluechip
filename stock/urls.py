from django.conf.urls import url

from .views import StockLV, main, stockDV, stock_search


urlpatterns = [
    url(r'^main/$', main, name='main'),
    url(r'^$', StockLV.as_view(), name='list'),
    url(r'^detail/(?P<code>[A-Za-z-0-9]+)/$', stockDV, name='stock_detail'),
    url(r'^search/$', stock_search, name='search'),
]
