from django.db import models

# Create your models here.
class UploadVideoModel(models.Model):
    title = models.TextField(default="")
    uploadedVideo = models.FileField(null=True)