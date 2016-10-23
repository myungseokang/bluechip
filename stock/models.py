from django.db import models

from accounts.models import InvestUser


class Stock(models.Model):
    business = models.CharField(max_length=30)
    title = models.CharField(max_length=20, unique=True, null=False)
    code = models.CharField(max_length=10, unique=True, null=False)

    # 전일
    yesterday_price = models.PositiveIntegerField(default=0)

    # 현재가
    price = models.PositiveIntegerField(default=0)

    # 시가
    today_start_price = models.PositiveIntegerField(default=0)

    # 상한가
    max_price = models.PositiveIntegerField(default=0)

    # 하한가
    min_price = models.PositiveIntegerField(default=0)

    # 고가
    high_price = models.PositiveIntegerField(default=0)

    # 저가
    low_price = models.PositiveIntegerField(default=0)

    # 등락률
    change = models.FloatField(default=0)

    def __str__(self):
        return self.title


class StockUser(models.Model):
    user = models.ForeignKey(InvestUser, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock)

