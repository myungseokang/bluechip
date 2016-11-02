from django import forms
from accounts.models import InvestUser
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

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
        fields = ["nickname", "username"]
        labels = {
            "username":"아이디",
        }

    def __init__(self, *args, **kwargs):
        super(Sing_upForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': ''})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(Sing_upForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
