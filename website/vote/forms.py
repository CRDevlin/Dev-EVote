from django import forms


class CommentForm(forms.Form):
    name = forms.CharField(label="Enter your token:",
                           widget=forms.PasswordInput,
                           null=True,
                           max_length=100)
