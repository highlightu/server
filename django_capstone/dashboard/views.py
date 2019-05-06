# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import *

from .models import MergedVideo
from main.models import User
from .forms import RequestForm  # , VideoForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse, Http404
import os
import requests
import re

thSize = {'width': '1168', 'height': '657'}
dateDict = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec',
}


def dashboard(request):
    keys = list(request.session.keys())
    if request.method == 'POST':  # if form is send by POST...
        form = RequestForm(request.POST)  # bind it to the request form
        if form.is_valid():  # if it has all attributes
            fullURL = form.cleaned_data['url']
            owner = form.cleaned_data['sender'].split('@')[0]

            vid = re.split("[/]", fullURL)[-1]
            print("Working VideoNumber is : " + vid)
            url = "https://player.twitch.tv/?autoplay=false&video=v" + vid

            request.session['videoNumber'] = int(vid)
            request.session['owner'] = owner

            # date
            date = str(timezone.localtime())
            date = re.split('[ ]', date)[0]
            date = re.sub('[-]', '.', date)
            request.session['today'] = date

            date = re.split("[.]",date)
            month = dateDict[date[1]]
            day = date[2]


            request.session['month'] = month
            request.session['day'] = day

            # Redirect after POST
            return render(request, 'mypage/dashboard.html', {
                'thumb': getThumb(vid),
            })
        else:
            return render(request, 'mypage/alert.html', {'msg': "Invalid Form was sent."})

    elif 'owner' in keys and 'videoNumber' in keys and 'today' in keys:
        return render(request, 'mypage/dashboard.html', {
            'thumb': getThumb(str(request.session['videoNumber'])),
        })
    # no session data nor valid post data
    return render(request, 'mypage/alert.html', {'msg': "잘못된 접근입니다"})



# def findUserInstance(user_name):
#     user_intance = User.objects.filter(user_name=F(user_name))
#     print('in FUI ' + user_intance)
#     return user_intance


def history(request):
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
    return render(request, 'mypage/history.html',{
        'merged_videos': myMergedVideoSet,
        'page':page,
        # "url": video_url,
    })

def download(request, id):
    keys = list(request.session.keys())
    if 'owner' not in keys:
        return render(request, 'mypage/alert.html', {'msg': "잘못된 접근입니다"})

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

def getVideoId(url):
    VideoId = url.split("/")[-1]
    return VideoId


def getThumb(videoId):
    # API요청을 보내기 위한 헤더
    TWITCH_CLIENT_ID = "37v97169hnj8kaoq8fs3hzz8v6jezdj"
    TWITCH_CLIENT_ID_HEADER = "Client-ID"
    TWITCH_V5_ACCEPT = "application/vnd.twitchtv.v5+json"
    TWITCH_V5_ACCEPT_HEADER = "Accept"
    TWITCH_AUTHORIZATION_HEADER = "Authorization"

    VIDEO_URL = "https://api.twitch.tv/kraken/videos/" + videoId

    headers = {TWITCH_CLIENT_ID_HEADER: TWITCH_CLIENT_ID,
               TWITCH_V5_ACCEPT_HEADER: TWITCH_V5_ACCEPT}

    # API 요청을 보낸다.
    video_request = requests.get(VIDEO_URL, headers=headers)
    video_request_json = video_request.json()

    # 썸네일 템플릿 url 획득
    thumb_template_url = str(video_request_json['preview']['template'])

    # 1920x1080크기의 썸네일 이미지를 얻는다.
    size = thSize

    return thumb_template_url.format(**size)

