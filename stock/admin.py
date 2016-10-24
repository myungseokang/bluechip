from django.contrib import admin
from stock.models import Stock, StockManager
# Register your models here.

admin.site.register(Stock)
admin.site.register(StockManager)
