from django.conf.urls import url

from .views import StockLV


urlpatterns = [
    url(r'^$', StockLV.as_view(), name='list'),
]
