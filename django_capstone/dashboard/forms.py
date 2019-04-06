from django import forms

class RequestForm(forms.Form):

    class Meta:
        fields=('url','sender')

    url = forms.CharField()
    sender = forms.EmailField()


class UploadOptionForm(forms.Form):

    class Meta:
        fields=('delay',
                'face',
                'speech',
                'chat',
                'youtube',
                'sender')

    delay = forms.IntegerField()
    face = forms.BooleanField()
    speech = forms.BooleanField()
    chat = forms.BooleanField()
    youtube = forms.BooleanField()
    sender = forms.EmailField()
