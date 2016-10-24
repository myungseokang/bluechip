from django import forms
from stock.models import Stock

class searchForm(forms.ModelForm):

    class Meta:
        model = Stock
        fields = ['title']
        labels = {
            'title':'종목 이름'
        }
