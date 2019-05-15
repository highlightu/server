# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import *

from .models import MergedVideo
from main.models import User

from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse, Http404
import os






# def findUserInstance(user_name):
#     user_intance = User.objects.filter(user_name=F(user_name))
#     print('in FUI ' + user_intance)
#     return user_intance


def archive(request):
    # check if the user is authorized
    user_instance = User.objects.filter(user_name=request.session['owner']).get()
    if user_instance is None:
        return HttpResponse("Unauthorized user")

    # Get result video set
    myMergedVideoSet = MergedVideo.objects.filter(owner=user_instance)
    if myMergedVideoSet is None:
        return HttpResponse("No video found")
    # video_url=myMergedVideoSet[0].video.url
    # pagination
    paginator = Paginator(myMergedVideoSet, 2)  # Show 2 video per page
    page = request.GET.get('page')
    myMergedVideoSet = paginator.get_page(page)
    return render(request, 'archive.html',{
        'merged_videos': myMergedVideoSet,
        'page':page,
        "MEDIA_URL": settings.MEDIA_URL
    })

def download(request, id):
    keys = list(request.session.keys())
    if 'owner' not in keys:
        return render(request, 'alert.html', {'msg': "잘못된 접근입니다"})

    target = MergedVideo.objects.filter(id=id)[0]
    file_path = target.video.path
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="video/mp4")
            response['Content-Disposition'] = 'attachment; filename=' +  os.path.basename(file_path)
            return response
    raise Http404

# def display_video(request,vid=None):
#     if vid is None:
#         return HttpResponse("No Video")
#
#     #Finding the name of video file with extension, use this if you have different extension of the videos
#     video_name = ""
#     for fname in os.listdir(settings.MEDIA_ROOT):
#         if fname.fnmatch(fname, vid+".*"): #using pattern to find the video file with given id and any extension
#             video_name = fname
#             break
#
#
#     '''
#         If you have all the videos of same extension e.g. mp4, then instead of above code, you can just use -
#
#         video_name = vid+".mp4"
#
#     '''
#
#     #getting full url -
#     video_url = settings.MEDIA_URL+video_name
#
#     return render(request, "video_template.html", {"url":video_url})


def payment(request):
    # check if the user is authorized
    user_instance = User.objects.filter(user_name=request.session['owner']).get()
    if user_instance is None:
        return HttpResponse("Unauthorized user")

    # Get result video set
    myMergedVideoSet = MergedVideo.objects.filter(owner=user_instance)
    if myMergedVideoSet is None:
        return HttpResponse("No video found")
    # video_url=myMergedVideoSet[0].video.url
    # pagination
    paginator = Paginator(myMergedVideoSet, 2)  # Show 2 video per page
    page = request.GET.get('page')
    myMergedVideoSet = paginator.get_page(page)
    return render(request, 'payment.html',{
        'merged_videos': myMergedVideoSet,
        'page':page,
        "MEDIA_URL": settings.MEDIA_URL
    })