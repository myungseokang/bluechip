from django.test import TestCase
from django.shortcuts import get_object_or_404

from .models import Stock


class StockTestCase(TestCase):
    def setUp(self):
        stock = Stock.objects.create(business='테스트', title='테스트', code='000000', price=100000)

    def test_stock_can_create(self):
        stock = get_object_or_404(Stock, title='테스트')
        self.assertEqual(stock.business, '테스트')
        self.assertEqual(stock.code, '000000')
