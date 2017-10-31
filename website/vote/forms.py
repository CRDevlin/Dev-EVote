from django import forms
from django.contrib.admin.widgets import AdminDateWidget


class TokenForm(forms.Form):
    token = forms.CharField(label='Enter your Token:', max_length=32, widget=forms.PasswordInput())


class VoteForm(forms.Form):
    CHOICES=[('1', 'Joe smoe'),
             ('2', 'Sally Two shoes')]

    choice = forms.ChoiceField(label='Candidates:', choices=CHOICES, widget=forms.RadioSelect())


class ElectionUploadForm(forms.Form):
    voter_file = forms.FileField(label='')
    nominee_file = forms.FileField(label='Nominees. Accepted file formats: .json')
    date = forms.DateTimeField(label='Date to Vote by')
    multi_vote = forms.BooleanField(label='Multi-Vote')
    anonymous = forms.BooleanField(label='Anonymous Voting')
