from event_crawling import business
from stock.models import Stock


def create_stock_data():
    stock_list = business()
    for stock in stock_list:
        new_stock = Stock()
        new_stock.business = stock['business']
        new_stock.code = stock['code']
        new_stock.title = stock['title']
        new_stock.graph_url()
        new_stock.stock_reset()
        new_stock.save()


def run():
    try:
        create_stock_data()
    except Exception as e:
        print(e)
