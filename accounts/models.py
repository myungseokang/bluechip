from django.db import models
from django.contrib.auth.models import AbstractUser
#from stock.models import StockManager


class InvestUser(AbstractUser):
    """
    모의 투자 유저
    """
    nickname = models.CharField("닉네임",max_length=100)
    money = models.IntegerField(default=100000)

    #def own_stock(self):
    #    flag_1 = StockManager.objects.filter(flag=1, user=self)
    #    own_stock = []
    #    title_name = []
    #    for i in flag_1:
    #        if i.title in title_name:
    #            continue
    #        title_name.append(i.title)
    #        own_stock.append({'title':i.title, 'price':i.price})
    #    return own_stock
