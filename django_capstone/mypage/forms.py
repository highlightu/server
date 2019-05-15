from django import forms
from .models import Video





class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = (
            'owner',
            'videoNumber',
            'delay',
            'face',
            'speech',
            'chat',
            'youtube',
            'date',
            'videoFileURL',
        )

        widgets = {
            'owner': forms.HiddenInput(),
            'videoNumber': forms.HiddenInput(),
            'delay': forms.HiddenInput(),
            'face': forms.HiddenInput(),
            'speech': forms.HiddenInput(),
            'chat': forms.HiddenInput(),
            'date': forms.HiddenInput(),
            'videoFileURL': forms.HiddenInput(),
        }
