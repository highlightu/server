from django.db import models
from main.models import User

# Create your models here.


class Video(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    Video_Number = models.IntegerField()

    def __str__(self):
        return self.owner

    class Meta:
        ordering = ('owner',)


class UploadOptionModel(models.Model):
    delay = models.IntegerField()
    face = models.BooleanField(default=False)
    speech = models.BooleanField(default=False)
    chat = models.BooleanField(default=False)
    youtube = models.BooleanField(default=False)
