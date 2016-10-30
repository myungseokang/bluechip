from django.db import models
from accounts.models import InvestUser

from bs4 import BeautifulSoup
import requests

class Stock(models.Model):
    business = models.CharField(max_length=30)
    title = models.CharField(max_length=20, unique=True, null=False)
    code = models.CharField(max_length=10, unique=True, null=False)

    yesterday_price = models.PositiveIntegerField(default=0, help_text="전일")
    price = models.PositiveIntegerField(default=0, help_text="현재가")
    today_start_price = models.PositiveIntegerField(default=0, help_text="시가")

    max_price = models.PositiveIntegerField(default=0, help_text="상한가")
    min_price = models.PositiveIntegerField(default=0, help_text="하한가")
    high_price = models.PositiveIntegerField(default=0, help_text="고가")
    low_price = models.PositiveIntegerField(default=0, help_text="저가")

    change = models.FloatField(default=0, help_text="등락률")
    deal = models.PositiveIntegerField(default=0, help_text="거래량")

    today_graph = models.URLField(max_length=200, default='', help_text="1일 그래프")
    month_graph = models.URLField(max_length=200, default='', help_text="1개월 그래프")
    three_month_graph = models.URLField(max_length=200, default='', help_text="3개월 그래프")
    year_graph = models.URLField(max_length=200, default='', help_text="1년 그래프")

    def __str__(self):
        return self.title

    def stock_reset(self):
        url = "http://finance.daum.net/item/main.daum"
        html_doc = requests.get(url, params={'code':self.code})
        html = BeautifulSoup(html_doc.text, 'html.parser')
        self.deal=int(html.find('ul',{'class':'list_stockrate'}).find_all('li')[4].span.text.replace(',', ''))
        self.change=float(html.find('ul',{'class':'list_stockrate'}).find_all('li')[2].text.replace('％',''))
        self.price=int(html.find('ul',{'class':'list_stockrate'}).li.em.text.replace(',', ''))
        stock_html = html.find('div', {'id':'stockContent'}).find_all('dl')
        for stock in stock_html:
            name = stock.dt.text
            quote = stock.dd.text.replace('\t', '').replace('\n', '').replace(',', '').replace('-','')
            if (name=="전일"):
                self.yesterday_price=int(quote)
            elif(name=='고가'):
                self.high_price=int(quote)
            elif(name=='저가'):
                self.low_price=int(quote)
            elif(name=='시가'):
                self.today_start_price=int(quote)
            elif(name=='상한가'):
                self.max_price=int(quote)
            elif(name=='하한가'):
                self.min_price=int(quote)
                self.save()
                break

    def graph_url(self):
        url = 'http://finance.daum.net/item/main.daum?nil_profile=vsearch&nil_src=stock'
        html_doc = requests.get(url, params={'code':self.code})
        html = BeautifulSoup(html_doc.text, 'html.parser')
        graphs = html.find('div', {'id':'stockGraph'}).find_all('img')
        self.today_graph = graphs[0].get('src')
        self.month_graph = graphs[1].get('src')
        self.three_month_graph = graphs[2].get('src')
        self.year_graph = graphs[3].get('src')
        self.save()

    def asking_price(self):
        url = "http://finance.daum.net/item/quote.daum"
        html_doc = requests.get(url, params={'code':self.code})
        html = BeautifulSoup(html_doc.text, 'html.parser')
        buy_prices = []  # 매수 호가
        sell_prices = [] # 매도 호가
        for sell_price in html.find('table', {'class':'mColor'}).find_all('tr')[1:]:
            try:
                sell = int(sell_price.find_all('td', {'class':'rColor3'})[1].text.replace(',', ''))
                sell_prices.append(sell)
            except:
                break
        for buy_price in html.find('table', {'class':'mColor'}).find_all('tr')[6:]:
            try:
                buy = int(buy_price.find_all('td', {'class':'bColor3'})[0].text.replace(',', ''))
                buy_prices.append(buy)
            except:
                break
        return buy_prices, sell_prices

    def about_stock(self, user):
        user_stock = self.stockmanager_set.filter(user=user, stock=self)
        print(user_stock)
        own_count  = request_buy = request_sell = 0
        for i in user_stock:
            i.conclusion()
            if i.request_flag==1 and i.flag==1:
                own_count+=i.count
            elif i.request_flag==1 and i.flag==0:
                request_buy += i.count
            elif i.request_flag == 0 and i.flag==0:
                request_sell += i.count
            elif i.request_flag == 0 and i.flag==1:
                own_count-=i.count
        return own_count, request_buy, request_sell



class StockManager(models.Model):
    user = models.ForeignKey(InvestUser, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock)

    request_flag = models.BooleanField(default=0,  help_text="요청 종류 0:매도, 1:매수")
    request_price = models.PositiveIntegerField(default=0,  help_text="요청 가격")
    count = models.PositiveIntegerField(default=0,  help_text="요청 개수")
    total_price = models.PositiveIntegerField(default=0, help_text="요청(가격X개수)")
    when_price = models.PositiveIntegerField(default=0,  help_text="요청 당시의 현재가")
    flag = models.BooleanField(default=0,  help_text="0:미체결, 1:체결")
    request_cancel = models.BooleanField(default=0, help_text="취소")
    user_money = models.PositiveIntegerField(default=0, help_text="신청 당시의 유저 금액")
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s_%s' %(self.user.nickname, self.stock.title)

    def sell(self, request_price, count):
        own_count = self.stock.about_stock(self.user)[0]
        if (own_count-count<0):
            self.delete()
            return "매도량>보유 주식"
        self.user_money = self.user.money
        self.request_flag = 0
        self.when_price = self.stock.price
        self.request_price = request_price
        self.count = count
        self.total_price = request_price*count
        self.save()
        return 1

    def buy(self, request_price, count):
        if(request_price==0):
            self.delete()
            return "유효한 호가가 아닙니다."
        if (self.user.money-(int(request_price)*int(count))<0):
            self.delete()
            return 'your money : %d\nstock price : %d\nerror' %(self.user.money, int(request_price)*int(count))
        self.request_flag = 1
        self.when_price = self.stock.price
        self.request_price = request_price
        self.count = count
        self.user.money-=(int(request_price)*int(count))
        self.user_money = self.user.money
        self.total_price = request_price*count
        self.save()
        self.user.save()
        return 1

    def buy_conclusion(self):
        if(self.flag==1):
            return
        if (self.stock.price==self.request_price or self.when_price==self.request_price):
            self.flag = 1
        if((self.stock.price>self.request_price and self.when_price<self.request_price)):
            self.flag = 1
        elif((self.stock.price<self.request_price and self.when_price>self.request_price)):
            self.flag = 1
        self.save()

    def sell_conclusion(self):
        if(self.flag==1):
            return
        if (self.stock.price==self.request_price or self.when_price==self.request_price):
            self.user.money += self.request_price*self.count
            self.flag = 1
        if((self.stock.price>self.request_price and self.when_price<self.request_price)):
            self.user.money += self.request_price*self.count
            self.flag = 1
        elif((self.stock.price<self.request_price and self.when_price>self.request_price)):
            self.user.money += self.request_price*self.count
            self.flag = 1
        self.save()
        self.user.save()

    def conclusion(self): # 이 함수가 알아서  매도, 매수 구별
        if(self.request_flag==1):
            self.buy_conclusion()
        elif(self.request_flag==0):
            self.sell_conclusion()

    def buy_cancel(self):
        if(self.request_flag!=1 and self.flag!=1 and self.request_cancel!=1):
            return
        self.user.money += self.total_price
        self.request_cancel = 1
        self.user.save()
        self.save()
        StockManager.objects.create(user=self.user, stock=self.stock, request_flag=0,
            request_price=self.request_price, count=self.count, total_price=self.total_price,
            request_cancel=1, user_money=self.user.money
        )

    def sell_cancel(self):
        if(self.request_flag!=0 and self.flag!=1 and self.request_cancel!=1):
            return
        self.request_cancel = 1
        self.save()

    def cancel(self):
        if(self.request_flag==1 and self.flag!=1 and self.request_cancel!=1):
            self.buy_cancel()
        elif(self.request_flag==0 and self.flag!=1 and self.request_cancel!=1):
            self.sell_cancel()
