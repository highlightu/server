from django import forms

class RequestForm(forms.Form):
    url = forms.CharField()
    sender = forms.EmailField()
