from django.db import models

from accounts.models import InvestUser

from bs4 import BeautifulSoup
import requests
import lxml

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

    # 거래량
    deal = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def stock_reset(self):
        url = "http://finance.daum.net/item/main.daum"
        html_doc = requests.get(url, params={'code':self.code})
        html = BeautifulSoup(html_doc.text, 'lxml')
        self.deal=int(html.find('ul',{'class':'list_stockrate'}).find_all('li')[4].span.text.replace(',', ''))
        self.change=float(html.find('ul',{'class':'list_stockrate'}).find_all('li')[2].text.replace('％',''))
        self.price=int(html.find('ul',{'class':'list_stockrate'}).li.em.text.replace(',', ''))
        stock_html = html.find('div', {'id':'stockContent'}).find_all('dl')
        for stock in stock_html:
            name = stock.dt.text
            quote = stock.dd.text.replace('\t', '').replace('\n', '').replace(',', '').replace('-','')
            if (name=="전일"):
                self.yesterday_priceint=int(quote)
            elif(name=='고가'):
                self.high_price=int(quote)
            elif(name=='저가'):
                self.low_price=int(quote)
            elif(name=='시가'):
                today_start_price=int(quote)
            elif(name=='상한가'):
                self.max_price=int(quote)
            elif(name=='하한가'):
                self.min_price=int(quote)
                self.save()
                break



class StockManager(models.Model):
    user = models.ForeignKey(InvestUser, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock)

    # 요청 종류 0 : 매도 1 : 매수
    request_flag = models.BooleanField(default=0)

    # 요청 가격
    request_price = models.PositiveIntegerField(default=0)

    # 요쳥했을 떄의 현재가
    when_price = models.PositiveIntegerField(default=0)

    # 요청 개수
    count = models.PositiveIntegerField(default=0)

    # 거래 상태
    flag = models.BooleanField(default=0)
