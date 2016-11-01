from django.conf.urls import url

from .views import term

urlpatterns = [
    url(r'^$', term, name='term')
]
