from django.conf.urls import url

from .views import StockLV, main


urlpatterns = [
    url(r'^main/$', main, name='main'),
    #url(r'^detail/(?P<code>[])')
    url(r'^$', StockLV.as_view(), name='list'),
]
