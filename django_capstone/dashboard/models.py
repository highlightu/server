from django.db import models
from main.models import User

# Create your models here.


class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    videoNumber = models.IntegerField()
    delay = models.IntegerField()
    face = models.BooleanField(default=False)
    speech = models.BooleanField(default=False)
    chat = models.BooleanField(default=False)
    youtube = models.BooleanField(default=False)
    date = models.CharField(max_length=50)
    videoFileURL = models.CharField(max_length=200)
    #thSize = {'width': '1168', 'height': '657'}
    resizing_start = models.IntegerField(default=1168)
    resizing_end = models.IntegerField(default=657)

    def __str__(self):
        return self.owner

    class Meta:
        ordering = ('owner',)
