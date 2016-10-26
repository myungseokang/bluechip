from event_crawling import business
from stock.models import Stock


def create_stock():
    stock_list = business()
    for stock in stock_list:
        Stock.objects.create(business=stock['business'], code=stock['code'], title=stock['title'])


def create_stock_data():
    stock_list = Stock.objects.all()
    for stock in stock_list:
        stock.graph_url()
        stock.stock_reset()


def run():
    try:
        create_stock()
        create_stock_data()
    except Exception as e:
        print(e)
