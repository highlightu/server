from django.db import models
from main.models import User
import os

# Create your models here.
def content_file_name(instance, filename):
    return os.path.join(instance.path,filename)

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
    title = models.CharField(max_length=100)
    rect_x = models.IntegerField(default=0)
    rect_y = models.IntegerField(default=0)
    rect_width = models.IntegerField(default=0)
    rect_height = models.IntegerField(default=0)


    def __str__(self):
        return self.owner

    class Meta:
        ordering = ('owner',)


class MergedVideo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    videoNumber = models.IntegerField()
    date = models.CharField(max_length=50)
    path = models.CharField(max_length=200, default="path")
    video = models.FileField(upload_to=content_file_name,max_length=500)
    title = models.CharField(max_length=100)
    # videoFileURL = models.CharField(max_length=200)

    def __str__(self):
        return self.owner

    class Meta:
        ordering = ('owner','date',)


class Order(models.Model):
    orderNo= models.CharField(max_length=36, primary_key=True)
    payToken= models.CharField(max_length=23)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.orderNo + ',' + self.payToken