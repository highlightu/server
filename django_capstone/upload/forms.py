from django import forms
from .models import VideoUploadModel
# Create your models here.
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUploadModel
        fields = ('title', 'videoFile')
