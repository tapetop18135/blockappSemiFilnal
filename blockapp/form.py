from django import forms


class Blockform(forms.Form):
    title = forms.CharField(max_length=100, label='title')
    content = forms.CharField(max_length=1000, label='content')