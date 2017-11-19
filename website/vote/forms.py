from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from .queries import *

class TokenForm(forms.Form):
    token = forms.CharField(label='Enter your Token:', max_length=32, widget=forms.PasswordInput())


class VoteForm(forms.Form):
    CHOICES = [('1', 'Test'), ('2', 'Test2')]
    choice = forms.ChoiceField(label='Candidates:', choices=CHOICES, widget=forms.RadioSelect)
    # def __init__(token):
    #    choice = forms.ModelChoiceField(label='Candidates:',
    #                                    queryset=Record.objects.get(token=token),
    #                                    widget=forms.RadioSelect())
    #    super.__init__()


class ElectionUploadForm(forms.Form):
    voter_file = forms.FileField()
    nominee_file = forms.FileField()
    date = forms.DateField(label='Date to Vote by', widget=AdminDateWidget)
    time = forms.TimeField(label='Time to Vote by', widget=AdminTimeWidget)
    multi_vote = forms.BooleanField(label='Multi-Vote', required=False)
    anonymous = forms.BooleanField(label='Anonymous Voting', required=False)
