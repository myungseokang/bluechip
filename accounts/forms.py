from django import forms
from accounts.models import InvestUser

class Sing_upForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=("비밀번호"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=("비밀번호 확인"),
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = InvestUser
        fields = ['nickname', 'username']
        labels = {
            "username":"아이디",
        }
    #def __init__(self, *args, **kwargs):
    #    super(forms.ModelForm, self).__init__(*args, **kwargs)
    #    self.fields['username'].label = "아이디"
