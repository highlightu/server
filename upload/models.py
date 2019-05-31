from django.db import models
import re, os


# Create your models here.

def content_file_name(instance, filename):
    return os.path.join(instance.path,filename)

class VideoUploadModel(models.Model):
    title = models.CharField(max_length=200, default="new video")
    path = models.CharField(max_length=200, default="path")
    videoFile = models.FileField(upload_to=content_file_name,max_length=500)
