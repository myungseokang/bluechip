"""invest_house URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from .views import Home, Sign_up
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Logout를 하면 /home URl에 연결하고싶었습니다.
    url(r'^accounts/logout/$', logout, {'next_page': '/home'}, name='logout'),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^sign-up', Sign_up.as_view(), name='sign-up'),

    url(r'^stock/', include('stock.urls', namespace='stock')),
]
