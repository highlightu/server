from django.db import models


# Create your models here.
class UploadOptionModel(models.Model):
    delay = models.IntegerField()
    face = models.BooleanField(default=False)
    speech = models.BooleanField(default=False)
    chat = models.BooleanField(default=False)
    youtube = models.BooleanField(default=False)

