from django import forms
from .models import VideoUploadModel
# Create your models here.
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUploadModel
        fields = ('title', 'videoFile')

    def __init__(self, *args, **kwargs):
        super(VideoUploadForm, self).__init__(*args, **kwargs)
        self.fields['videoFile'].required = False
