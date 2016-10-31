from django.conf.urls import url

from .views import tutorial_1

urlpatterns = [
    url(r'^one/$', tutorial_1, name='tutorial_1')
]
