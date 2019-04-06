from django.db import models
from main.models import User

# Create your models here.


class UploadOptionModel(models.Model):
    delay = models.IntegerField()
    face = models.BooleanField(default=False)
    speech = models.BooleanField(default=False)
    chat = models.BooleanField(default=False)
    youtube = models.BooleanField(default=False)


class Video(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    Video_ID = models.IntegerField(default=0, editable=False)
