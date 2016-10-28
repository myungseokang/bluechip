from django_cron import CronJobBase, Schedule
from stock.models import Stock, StockManager

class reset(CronJobBase):
    RUN_EVERY_MINS = 10
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'stock.reset'

    def do(self):
        stocks = Stock.objects.all()
        for stock in stocks:
            stock.stock_reset()
        request_stocks = StockManager.objects.filter(flag=0)
        for request_stock in request_stocks:
            request_stock.conclusion()
