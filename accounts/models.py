from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
#from stock.models import StockManager


class InvestUser(AbstractUser):
    """
    모의 투자 유저
    """
    nickname = models.CharField("닉네임",max_length=100)
    money = models.IntegerField(default=100000)
    take_price = models.IntegerField(default=0, help_text="보유 주식 가치")
    take_count = models.PositiveIntegerField(default=0, help_text="보유 주식의 수")
    total_money = models.IntegerField(default=0, help_text="보유 주식 가치 + money")

    def own_stock(self):
        flag_1 = self.stockmanager_set.filter(Q(request_flag=1,flag=1) | Q(request_flag=0, flag=1)).exclude(request_cancel=1)
        own_stock = []
        title_name = []
        for i in flag_1:
            if i.stock.title in title_name:
                number = title_name.index(i.stock.title)
                if i.request_flag==1 and i.flag==1:
                    own_stock[number]['count']+=i.count
                elif i.request_flag==0 and i.flag==1:
                     own_stock[number]['count']-=i.count
                continue
            context = {
                'title':i.stock.title,
                'price':i.stock.price,
                'code':i.stock.code,
                'count':i.count,
                'flag':i.flag,
                'request_flag':i.request_flag
            }
            title_name.append(i.stock.title)
            own_stock.append(context)
        return own_stock

    def log_stock(self):
        log = self.stockmanager_set.filter(user=self).exclude(request_cancel=1).order_by('-create_time')
        for stock in log:
            stock.stock.stock_reset()
            stock.conclusion()
        return log

    def total_money_reset(self):
        stocks = self.stockmanager_set.filter(request_flag=1, flag=1)
        self.total_money = 0
        self.take_count = 0
        for stock in stocks:
            self.total_money += stock.stock.price * stock.count
            self.take_count += stock.count
        self.take_price = self.total_money
        self.total_money += self.money
        self.save()
