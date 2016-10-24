from django.conf.urls import url

from .views import StockLV, main, stockDV


urlpatterns = [
    url(r'^main/$', main, name='main'),
    url(r'^detail/(?P<code>[0-9]+)/$', stockDV, name='stock_detail'),
    url(r'^$', StockLV.as_view(), name='list'),
]
