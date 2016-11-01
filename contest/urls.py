from django.conf.urls import url

from .views import contest

urlpatterns=  [
    url(r'^$', contest, name='contest'),
]
