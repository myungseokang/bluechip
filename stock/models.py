from django.db import models

from accounts.models import InvestUser


class Stock(models.Model):
    business = models.CharField(max_length=30)
    title = models.CharField(max_length=20, unique=True, null=False)
    code = models.CharField(max_length=10, unique=True, null=False)
    price = models.PositiveSmallIntegerField()
    user = models.ManyToManyField(InvestUser, through='StockUser', blank=True)

    def __str__(self):
        return self.title


class StockUser(models.Model):
    user = models.ForeignKey(InvestUser, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock)

