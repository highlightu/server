from django import forms
from .models import VideoUploadModel



# Create your models here.
class RequestForm(forms.Form):
    class Meta:
        fields = ('url', 'sender')

    url = forms.CharField()
    sender = forms.EmailField()



class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUploadModel
        fields = ('title', 'path', 'videoFile')

        widgets = {
            'path': forms.HiddenInput(),
        }
