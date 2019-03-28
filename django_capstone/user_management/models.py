from django.db import models
#from django.forms import ValidationError

# Create your models here.


class User(models.Model):
    # unique id for each User object will be automatically created
    email_address = models.EmailField(verbose_name='email',
                                      max_length=255,
                                      unique=True,)

class Channel(models.Model):
    channel_id = models.IntegerField(max_length=8)
    channel_name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)


class Fps(models.Model):
    p1080 = models.CharField(max_length=16)
    p720 = models.CharField(max_length=16)
    p480 = models.CharField(max_length=16)
    p360 = models.CharField(max_length=16)
    p244 = models.CharField(max_length=16)
    p144 = models.CharField(max_length=16)


class Segment(models.Model):
    duration = models.IntegerField(max_length=3)
    offset = models.IntegerField(max_length=10)


class Video(models.Model):
    streamer = models.ForeignKey(
        User, verbose_name=("streamer"), on_delete=models.CASCADE)
    client_id = models.CharField(max_length=15)
    broadcast_id = models.IntegerField(max_length=1)
    broadcast_type = models.CharField(max_length=15)
    channel = models.ForeignKey(Channel, verbose_name=(
        "channel"), on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    description_html = models.CharField(max_length=50)
    game = models.CharField(max_length=30)
    language = models.CharField(max_length=10)
    length = models.IntegerField(max_length=10)
