from django import forms


class TokenForm(forms.Form):
    token = forms.CharField(label='Enter your Token', max_length=32, widget=forms.PasswordInput())


