from django.conf.urls import url

from .views import tutorial_1,tutorial_2,tutorial_3,tutorial_4,tutorial_5,tutorial_6,tutorial_7,tutorial_8,tutorial_9,tutorial_10

urlpatterns = [
    url(r'^1/$', tutorial_1, name='1'),
    url(r'^2/$', tutorial_2, name='2'),
    url(r'^3/(?P<stock>.+)/$', tutorial_3, name='3'),
    url(r'^4/(?P<stock>.+)/(?P<price1>[0-9]+)/$', tutorial_4, name='4'),
    url(r'^5/(?P<stock>.+)/(?P<price1>[0-9]+)/$', tutorial_5, name='5'),
    url(r'^6/(?P<stock>.+)/(?P<price1>[0-9]+)/$', tutorial_6, name='6'),
    url(r'^7/(?P<stock>.+)/(?P<price1>[0-9]+)/$', tutorial_7, name='7'),
    url(r'^8/(?P<stock>.+)/(?P<price1>[0-9]+)/(?P<price2>[0-9]+)/$', tutorial_8, name='8'),
    url(r'^9/(?P<stock>.+)/(?P<price1>[0-9]+)/(?P<price2>[0-9]+)/$', tutorial_9, name='9'),
    url(r'^10/(?P<stock>.+)/(?P<price1>[0-9]+)/(?P<price2>[0-9]+)/$', tutorial_10, name='10'),
]
