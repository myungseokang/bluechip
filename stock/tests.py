from django.test import TestCase

from .models import Stock


class StockTestCase(TestCase):
    def setUp(self):
        self.business = '테스트 비즈니스'
        self.title = '테스트타이틀'
        self.code = '000000'
        self.price = 100000

    def test_stock_can_create(self):
        stock = Stock.objects.create(business=self.business, title=self.title, code=self.code, price=self.price)
        stock = Stock.objects.get(title=self.title)
        self.assertEqual(stock.business, self.business)
        self.assertEqual(stock.code, self.code)
