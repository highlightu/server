from django import forms
from .models import UploadVideoModel

# Create your models here.
class UploadVideoForm(forms.ModelForm):
    class Meta:
        model = UploadVideoModel
        fields = ('title','uploadedVideo')

    def __init__(self, *args, **kwargs):
        super(UploadVideoForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False