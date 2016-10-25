from django import forms
from stock.models import Stock

class searchForm(forms.ModelForm):

    class Meta:
        model = Stock
        fields = ['title']
        labels = {
            'title':'종목 이름'
        }

MY_CHOICES = (
    ('0', '매도'),
    ('1', '매수'),
)

class requestForm(forms.Form):
    request_flag = forms.ChoiceField(choices=MY_CHOICES)
    request_price = forms.IntegerField(max_value=10000000)
    count = forms.IntegerField(max_value=100)
