from django.db import models



# Create your models here.
class VideoUploadModel(models.Model):
    title = models.CharField(max_length=200, default="new video")
    videoFile = models.FileField()
