from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget


class ElectionResTokenForm(forms.Form):
    """
    Form for authenticating an administrator to see the results of an election
    """
    def __init__(self, token_len, *args, **kwargs):
        super(ElectionResTokenForm, self).__init__(*args, **kwargs)
        self.fields['token'] = forms.CharField(label='Enter the Election Token:', max_length=token_len, widget=forms.PasswordInput())


class VoteTokenForm(forms.Form):
    """
    Form for authenticating a faculty member to vote
    """
    def __init__(self, token_len, *args, **kwargs):
        super(VoteTokenForm, self).__init__(*args, **kwargs)
        self.fields['token'] = forms.CharField(label='Enter your Token:', max_length=token_len, widget=forms.PasswordInput())


class VoteForm(forms.Form):
    """
    Form for a voter to choose from a potential list of candidates.
    """
    def __init__(self, choices, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.ChoiceField(label='Candidates:', choices=choices, widget=forms.RadioSelect)


# TODO: Implement AdminDateWidget and AdminTimeWidget
class ElectionUploadForm(forms.Form):
    """
    Form for creating a new election.
    """
    voter_file = forms.FileField()
    nominee_file = forms.FileField()
    date = forms.DateField(label='Date to Vote by', widget=AdminDateWidget)
    time = forms.TimeField(label='Time to Vote by', widget=AdminTimeWidget)
    multi_vote = forms.BooleanField(label='Multi-Vote', required=False)
    anonymous = forms.BooleanField(label='Anonymous Voting', required=False)
