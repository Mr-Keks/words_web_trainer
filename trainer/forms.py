from django import forms


class WordForm(forms.Form):
    word = forms.CharField(label='', max_length=50, )
    target = forms.CharField(label='', max_length=50, required=None)
    