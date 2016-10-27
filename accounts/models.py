from django.db import models
from django.contrib.auth.models import AbstractUser
#from stock.models import StockManager


class InvestUser(AbstractUser):
    """
    모의 투자 유저
    """
    nickname = models.CharField("닉네임",max_length=100)
    money = models.IntegerField(default=100000)

    def own_stock(self):
        flag_1 = self.stockmanager_set.filter(request_flag=1,flag=1).filter(request_flag=0)
        own_stock = []
        title_name = []
        for i in flag_1:
            if i.stock.title in title_name:
                number = title_name.index(i.stock.title)
                if i.request_flag==1 and i.flag==1:
                    own_stock[number]['count']+=i.count
                elif i.reques_flag==0:
                     own_stock[number]['count']-=i.count
                continue
            context = {
                'title':i.stock.title,
                'price':i.stock.price,
                'count':i.count,
                'flag':i.flag,
                'request_flag':i.request_flag
            }
            title_name.append(i.stock.title)
            own_stock.append(context)
        return own_stock

    def log_stock(self):
        log = self.stockmanager_set.filter(user=self).order_by('-create_time')
        return log
